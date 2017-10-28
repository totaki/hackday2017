from pprint import pprint

from natasha import (NamesExtractor, DatesExtractor, MoneyExtractor, LocationExtractor, AddressExtractor,
                     OrganisationExtractor, PersonExtractor)

from utils import get_text


class NamedEntitiesExtractor:
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

    def match_to_dict(self, match):
        pass

    def process(self, text_object):
        text = get_text(text_object)
        result = []
        for extractor in self.extractors:
            result.extend(self.extract(text, extractor))
        text_object.update(
            {'named_entities': result})
        return result


if __name__ == '__main__':
    extractors = NamedEntitiesExtractor()
    text = '''
    Простите, еще несколько цитат из приговора. одна копейка «…Отрицал существование
    Иисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами
    ожившего мертвеца — зомби» [и] «качествами покемонов —
    представителей бестиария японской мифологии, тем самым совершил
    преступление, предусмотренное статьей 148 УК РФ от 1 декабря 2017 года
    '''
    text_object = {'text': text}
    pprint(extractors.extract_all(text))