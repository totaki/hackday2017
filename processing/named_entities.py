from natasha import (NamesExtractor, DatesExtractor, MoneyExtractor, LocationExtractor, AddressExtractor,
                     OrganisationExtractor, PersonExtractor)


class NamedEntitiesExtractorsLoader:
    date = None
    money = None
    location = None
    address = None
    organization = None
    person = None

    def __init__(self):
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

