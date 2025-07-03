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
                with open(file_path, 'w', encoding='utf-8') as f:
                    self._write_clean_json(item['full_code'], f)

            elif action == "modify":
                logging.info(f"Mengubah file {file_path}")
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
        Mengubah string JSON menjadi dict lalu tulis kembali ke file
        tanpa karakter escape (misal: \n), dalam format rapi.
        """
        try:
            json_obj = json.loads(json_str)  # parse string JSON
            json.dump(json_obj, file_obj, ensure_ascii=False, indent=2)  # simpan rapi
        except json.JSONDecodeError as e:
            logging.error(f"Gagal parse JSON dari full_code: {e}")
            file_obj.write(json_str)  # fallback tulis mentah
