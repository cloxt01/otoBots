import json
import os
import traceback
import logging
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from urllib.parse import urlparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class Sniffer:
    def __init__(self, conf):
        self.url = conf['url']
        self.api_domain = conf['api']['domain']
        self.logPath = None
        self.headless = conf['browser']['headlessMode']
        self.profile_path = conf['browser']['profilePath']
        self.data_log = {}

    def is_valid_api_request(self, url):
        parsed = urlparse(url)
        return self.api_domain in parsed.netloc

    async def handle_request(self, request):
        url = request.url
        if not self.is_valid_api_request(url):
            return

        timestamp = datetime.now().isoformat()
        try:
            headers = dict(request.headers)
            post_data = None
            # Gunakan async jika post_data() adalah fungsi
            try:
                if callable(getattr(request, "post_data", None)):
                    post_data = await request.post_data()
                else:
                    post_data = request.post_data
            except Exception as e:
                logging.warning(f"Gagal ambil post_data: {e}")

            self.data_log[url] = {
                "timestamp": timestamp,
                "url": url,
                "method": request.method,
                "request_headers": headers,
                "post_data": post_data,
                "response_status": None,
                "response_headers": None,
                "response_body": None
            }
        except Exception as e:
            logging.error(f"Error saat memproses request: {e}")
            logging.debug(traceback.format_exc())

    async def handle_response(self, response):
        url = response.url
        if not self.is_valid_api_request(url):
            return

        try:
            body = None
            content_type = (response.headers.get("content-type") or "").lower()

            try:
                if "application/json" in content_type:
                    try:
                        body = await response.json()
                    except Exception as e_json:
                        # Jika gagal JSON decode, capture sebagai text
                        body = await response.text()
                        logging.warning(f"[{response.status}] Tidak bisa decode JSON di {url}: {e_json}")
                elif any([
                    c in content_type for c in [
                        "text/", "application/javascript", "application/xml",
                        "application/x-www-form-urlencoded", "application/xhtml+xml",
                        "application/svg+xml"
                    ]
                ]):
                    try:
                        body = await response.text()
                    except Exception as e_text:
                        body = f"<text decode error: {e_text}>"
                elif any([
                    c in content_type for c in [
                        "image/", "font/", "application/octet-stream", "application/zip",
                        "application/pdf"
                    ]
                ]):
                    try:
                        # Simpan ringkasan saja (misal size byte)
                        resp_bytes = await response.body()
                        body = f"<{content_type} {len(resp_bytes)} bytes>"
                    except Exception as e_bin:
                        body = f"<binary decode error: {e_bin}>"
                else:
                    try:
                        # Tetap coba ambil text, fallback ke bytes summary jika error
                        body = await response.text()
                    except Exception:
                        try:
                            resp_bytes = await response.body()
                            body = f"<unknown binary {len(resp_bytes)} bytes>"
                        except Exception as e:
                            body = f"<unknown binary decode error: {e}>"
            except Exception as e:
                body = f"<unhandled error: {e}>"
                logging.warning(f"[{response.status}] Gagal memproses response di {url}: {e}")

            if url not in self.data_log:
                self.data_log[url] = {
                    "timestamp": datetime.now().isoformat(),
                    "url": url,
                    "method": None,
                    "request_headers": None,
                    "post_data": None
                }

            self.data_log[url].update({
                "response_status": response.status,
                "response_headers": dict(response.headers),
                "response_body": body
            })
        except Exception as e:
            logging.error(f"Error saat memproses response: {e}")
            logging.debug(traceback.format_exc())

    async def run(self):
        save_dir = "log"
        wib = timezone(timedelta(hours=7))
        now = datetime.now(wib)
        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
        self.logPath = os.path.join(save_dir, filename)


        try:
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            async with async_playwright() as p:
                browser = None
                try:
                    browser = await p.firefox.launch_persistent_context(
                        user_data_dir=self.profile_path,
                        headless=self.headless,
                        ignore_https_errors=True,
                        user_agent="Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0"
                    )
                    page = browser.pages[0] if browser.pages else await browser.new_page()

                    logging.info("Monitoring diaktifkan.")
                    page.on("request", lambda req: asyncio.create_task(self.handle_request(req)))
                    page.on("response", lambda res: asyncio.create_task(self.handle_response(res)))

                    logging.info(f"Menuju URL: {self.url}")
                    try:
                        await page.goto(self.url, timeout=60000)
                    except PlaywrightTimeoutError as e:
                        logging.error(f"Timeout saat akses URL: {e}")
                        logging.debug(traceback.format_exc())
                        return
                    except PlaywrightError as e:
                        logging.error(f"Playwright error saat akses URL: {e}")
                        logging.debug(traceback.format_exc())
                        return
                    except Exception as e:
                        logging.error(f"Error umum saat page.goto: {e}")
                        logging.debug(traceback.format_exc())
                        return

                    try:

                        loop = asyncio.get_event_loop()
                        logging.info("Tekan Enter untuk berhenti...")
                        await loop.run_in_executor(None, input)

                    except Exception as e:
                        logging.warning(f"Gagal saat menunggu input: {e}")
                        logging.debug(traceback.format_exc())
                finally:
                    if browser:
                        await browser.close()

            try:
                combined = list(self.data_log.values())
                with open(self.logPath, "w", encoding="utf-8") as f:
                    json.dump(combined, f, indent=2, ensure_ascii=False)
                logging.info(f"Log berhasil disimpan di {self.logPath}")
            except Exception as e:
                logging.error(f"Gagal menyimpan log ke file: {e}")
                logging.debug(traceback.format_exc())
        except Exception as e:
            logging.critical(f"Error fatal di run(): {e}")
            logging.debug(traceback.format_exc())