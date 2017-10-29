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
                "fact": match.fact.as_json
            })
        return result

    def process(self, text_object):
        text = get_text(text_object)
        result = []
        for extractor in self.extractors:
            result.extend(self.extract(text, extractor))
        text_object.update(
            {'named_entities': result})
        return text_object
