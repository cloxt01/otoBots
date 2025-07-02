import os

class Analyzer:

    def __init__(self, generator, sniffer):
        self.generator = generator
        self.sniffer = sniffer

    def analyze(self, prompt, image=None, filePath=None):
        analyze = self.generator.generate(prompt, image, filePath)
        return analyze