import logging

from conf.config import *
from generator.generator import *
from processor.processor import Processor
from sniffer.sniffer import *

if __name__ == "__main__":
    conf = loadConf()
    prompt = {
        "system": """
        Kamu diberikan sebuah direktori khusus bernama "content/". Tugasmu adalah membuat script bot flashsale otonom yang siap pakai berbahasa PYTHON, mulai dari membuat struktur file, menulis kode setiap file, hingga memberikan output aksi file sesuai parameter.

        Contoh parameter aksi yang dapat digunakan:
        {
            "action": "modify",
            "file": "main.py",
            "full_code": "import ...."
        }
        {
            "action": "make",
            "file": "content/main.py",
            "full_code": "import ..."
        }
        {
            "action": "remove",
            "file": "main.py"
        }

        Format output yang diharapkan (JSON):
        {
          "explained": "",
          "content": [
            {
              "action": "modify",
              "file": "main.py",
              "full_code": "import ...."
            }
          ]
        }

        Keterangan:
        - Kolom "explained" dapat diisi keterangan singkat mengenai aksi, atau dibiarkan kosong bila tidak perlu penjelasan.
        - Array "content" berisi list aksi (make/modify/remove) terhadap file sesuai kebutuhan workflow.
        - Sertakan "full_code" jika action make/modify.

        Output HARUS disusun persis seperti format json di atas, TANPA PENJELASAN tambahan lain di luar JSON !!!.

        Output Salah:
        Berikut struktur dan kode bot flashsale Tokopedia:
        {
            "explained":"...",
            "content":[]
        }

        Output Benar:
        {
            "explained":"...",
            "content":[]
        }
        """,
        "user": "MULAI"
    }


    sniffer = Sniffer(conf)
    asyncio.run(sniffer.run())


    generator = Generator(conf, "deepseek/deepseek-r1-0528:free")
    data = generator.generate(prompt, imagePath=None, filePath=sniffer.sniffer_log_path)


    processor = Processor(conf)
    processor.process(data)
