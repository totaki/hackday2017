from pyaspeller.speller import YandexSpeller


class Speller(YandexSpeller):
    def process(self, text):
        spelled_text = self.spell(text)
        for item in spelled_text:
            print(item)
            text = text.replace(item['word'], item['s'][0])
        return text


if __name__ == '__main__':
    text = """
    я вшел из дома кагда во всех онах
    """
    speller = Speller()
    print(speller.process(text))
