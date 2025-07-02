import json
import traceback
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
def loadConf():
    try:
        logging.info("Memuat config...")
        with open('conf/conf.json') as f:
            config = json.load(f)
            logging.info("Config dimuat")
            return config
    except Exception as e:
        print(f"Error saat memuat config: {e}")