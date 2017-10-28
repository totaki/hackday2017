from natasha import (NamesExtractor, DatesExtractor, MoneyExtractor, LocationExtractor, AddressExtractor,
                     OrganisationExtractor, PersonExtractor)


class NamedEntitiesExtractorsLoader:
    dates_extractor = None
    money_extractor = None
    location_extractor = None
    address_extractor = None
    organization_extractor = None
    person_extractor = None

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

