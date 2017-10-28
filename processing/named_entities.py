from natasha import (NamesExtractor, DatesExtractor, MoneyExtractor, LocationExtractor, AddressExtractor,
                     OrganisationExtractor, PersonExtractor)


class NamedEntitiesExtractor:
    dates_extractor = None
    money_extractor = None
    location_extractor = None
    address_extractor = None
    organization_extractor = None
    person_extractor = None

    def __init__(self):
        self.dates_extractor = DatesExtractor()
        self.names_extractor = NamesExtractor()
        self.money_extractor = MoneyExtractor()
        self.location_extractor = LocationExtractor()
        self.address_extractor = AddressExtractor()
        self.organization_extractor = OrganisationExtractor()
        self.person_extractor = PersonExtractor()

    def extract_dates(self, text):
        result = []
        matches = self.dates_extractor(text)
        for match in matches:
            result.append({
                "span": match.span,
                "fact": match.fact
            })
        return result
