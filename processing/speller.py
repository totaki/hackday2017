from pyaspeller.speller import YandexSpeller


class Speller(YandexSpeller):
    def process(self, text):
        spelled_text = self.spell(text)
        for item in spelled_text:
            text = text.replace(item['word'], item['s'][0])
        return text
