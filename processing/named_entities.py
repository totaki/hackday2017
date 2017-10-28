from pprint import pprint

from natasha import (NamesExtractor, DatesExtractor, MoneyExtractor, LocationExtractor, AddressExtractor,
                     OrganisationExtractor, PersonExtractor)


class NamedEntitiesExtractorsLoader:
    extractors = []
    date = None
    money = None
    location = None
    address = None
    organization = None
    person = None

    def __init__(self):
        self.extractors = ['date', 'money', 'location', 'address', 'organization', 'person']
        self.date = DatesExtractor()
        self.name = NamesExtractor()
        self.money = MoneyExtractor()
        self.location = LocationExtractor()
        self.address = AddressExtractor()
        self.organization = OrganisationExtractor()
        self.person = PersonExtractor()

    def extract(self, text, extractor):
        result = []
        matches = getattr(self, extractor)(text)
        for match in matches:
            result.append({
                "span": match.span,
                "fact": match.fact
            })
        return result

    def extract_all(self, text):
        result = []
        for extractor in self.extractors:
            result.extend(self.extract(text, extractor))
        return result


if __name__ == '__main__':
    extractors = NamedEntitiesExtractorsLoader()
    text = '''
    Простите, еще несколько цитат из приговора. одна копейка «…Отрицал существование
    Иисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами
    ожившего мертвеца — зомби» [и] «качествами покемонов —
    представителей бестиария японской мифологии, тем самым совершил
    преступление, предусмотренное статьей 148 УК РФ от 1 декабря 2017 года
    '''
    pprint(extractors.extract_all(text))