import os
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class Processor:

    def __init__(self, conf):
        self.content_path = conf['path']['content']

    def process(self, data: dict):
        for item in data.get('content', []):
            action = item.get('action')
            file_path = os.path.join(item['file'])

            if action == "make":
                logging.info(f"Membuat file {file_path}")
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    self._write_clean_json(item['full_code'], f)

            elif action == "modify":
                logging.info(f"Mengubah file {file_path}")
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    self._write_clean_json(item['full_code'], f)

            elif action == "remove":
                logging.info(f"Menghapus file {file_path}")
                if os.path.exists(file_path):
                    os.remove(file_path)

            else:
                logging.warning(f"Action tidak diketahui: {action}")

    def _write_clean_json(self, json_str, file_obj):
        """
        Menulis langsung kode mentah ke file tanpa parsing sebagai JSON.
        """
        try:
            file_obj.write(json_str)
        except Exception as e:
            logging.error(f"Gagal menulis full_code: {e}")