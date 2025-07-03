import json
import os, mimetypes, time
from pathlib import Path
from datetime import datetime, timedelta, timezone
import requests
import logging
import base64

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class Generator:
    def __init__(self, conf, model):
        self.log_path = conf['path']['log']
        self.conf = conf
        self.model = model
        self.max_tokens = conf['ai']['maxTokens']
        self.apiKey = self.load_apiKey(conf)
        if not self.apiKey or self.apiKey == "":
            logging.error("API Key tidak ditemukan. Generator tidak dapat digunakan.")

    def load_apiKey(self, conf):
        try:
            logging.info("Memuat API key...")
            if conf['ai']['apiKey']:
                logging.info("API Key dimuat")
                return conf['ai']['apiKey']
            return None
            # for plat_dict in conf['ai']['platform']:
            #     if self.platform in plat_dict:
            #         api_datas = plat_dict[self.platform]
            #         if api_datas and "apiKey" in api_datas[0]:
            #             logging.info("API Key berhasil dimuat")
            #             return api_datas[0]["apiKey"]
            # logging.warning(f"Tidak menemukan API key untuk platform: {self.platform}")
            # return None

        except Exception as e:
            logging.error(f"Error saat memuat API key: {e}")
            return None

    @staticmethod
    def get_data_url_prefix(path):
        mime, _ = mimetypes.guess_type(path)
        if mime is None:
            mime = "application/octet-stream"
        return mime


    def save_log(self, data):
        Path(self.log_path).mkdir(parents=True, exist_ok=True)

        wib = timezone(timedelta(hours=7))
        now = datetime.now(wib)

        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + "(generator).json"

        full_path = os.path.join(self.log_path, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def encodeBase64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def generate(self, prompt: dict, imagePath: str = None, filePath: str = None):
        try:
            logging.info("AI Thinking...")
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.apiKey}",
                "Content-Type": "application/json"
            }

            # Gabungkan prompt dan isi file menjadi satu string untuk user
            user_content = prompt['user']
            if filePath:
                with open(filePath, "r", encoding="utf-8") as f:
                    file_content = f.read()
                user_content += f"\n-----------------\n\n{file_content}\n\n-----------------\n"

            payload = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": [
                    {
                        "role": "system",
                        "content": prompt['system']   # string BUKAN dict
                    },
                    {
                        "role": "user",
                        "content": user_content      # string gabungan prompt+file
                    }
                ]
            }

            # Jika imagePath diisi, gunakan format multimodal (untuk model multimodal SAJA!)
            if imagePath:
                payload["messages"][1]["content"] = [
                    {
                        "type": "text",
                        "text": user_content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{self.get_data_url_prefix(imagePath)};base64,{self.encodeBase64(imagePath)}"
                        }
                    }
                ]

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                logging.error(f"Request gagal! Status: {response.status_code}, Response: {response.text}")
                return None
            try:
                self.save_log(response.json())
                res = response.json()["choices"][0]["message"]["content"]
                res = json.loads(res)
                return res
            except Exception as e:
                logging.error(f"Format response tidak valid: {e}. Response: {response.text}")
                return None
        except Exception as e:
            logging.error(f"Error saat membuat request: {e}")
            return None

