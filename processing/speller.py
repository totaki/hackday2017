from concurrent.futures import ThreadPoolExecutor

from pyaspeller.speller import YandexSpeller
from tornado.concurrent import run_on_executor

from utils import get_text


class Speller(YandexSpeller):
    executor = ThreadPoolExecutor(max_workers=5)

    @run_on_executor
    def process(self, text_object):
        text = get_text(text_object)
        spelled_text = self.spell(text)
        for item in spelled_text:
            text = text.replace(item['word'], item['s'][0])
        text_object.update({"prep_text": text})
        return text_object


if __name__ == '__main__':
    text = {"text": """
    я вшел из дома кагда во всех онах
    """}
    speller = Speller()
    print(speller.process(text))
