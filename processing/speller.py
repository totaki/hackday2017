from pyaspeller.speller import YandexSpeller

from utils import get_text


class Speller(YandexSpeller):
    def process(self, text_object):
        text = get_text(text_object)
        spelled_text = self.spell(text)
        for item in spelled_text:
            text = text.replace(item['word'], item['s'][0])
        text_object.update({"prep_text": text})
        return text_object


if __name__ == '__main__':
    text = """
    я вшел из дома кагда во всех онах
    """
    speller = Speller()
    print(speller.process(text))
