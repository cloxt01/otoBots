import asyncio

from conf.config import *
from generator.generator import *
from sniffer.sniffer import *
from analyzer.analyzer import *


if __name__ == "__main__":
    conf = loadConf()

    generator = Generator(conf, "deepseek/deepseek-r1-0528:free")

    sniffer = Sniffer(conf)
    asyncio.run(sniffer.run())

    analyzer = Analyzer(generator, sniffer)
    prompt = {
        "system": "You are a helpful assistant.",
        "user": "Tolong analisa traffic ini !"
    }
    print(analyzer.analyze(prompt, image=None, filePath=sniffer.logPath))


