from daft_scraper.listing import Listing
from daft_scraper.search import DaftSearch, SearchType
from daft_scraper.search.options_location import LocationsOption, Location


class DaftResults():
    def __init__(self, event):
        self.options = [
            LocationsOption([
                Location(loc)
                for loc in event['locations']
            ])
        ]
        self.search_type = SearchType(event['search_type'])
        self.max_pages = event['max_pages']
        self.daft = DaftSearch(self.search_type)

    def get_listings_as_rows(self):
        results = self.daft.search(self.options, max_pages=self.max_pages)
        return [
            DaftListing(listing).data
            for listing in results
        ]


class DaftListing(object):
    FIELDS = {
        'id': None,
        'title': str,
        'price': float,
        'url': str,
        'sections.0': str,
        'sections.1': str,
        'sections.2': str,
        'featuredLevel': str,
        'publishDate': None,
        'category': str,
        'numBedrooms': int,
        'numBathrooms': int,
        'propertyType': str,
        'media.totalImages': int,
        'media.hasBrochure': str,
        'media.hasVirtualTour': str,
        'ber.rating': str,
        'description': str,
        'county.0': str,
        'area.0': str,
        'views': int,
        'point.coordinates.0': float, # longitude
        'point.coordinates.1': float, # latitude
    }
    data = None
    def __init__(self, listing: Listing):
        self.data = {}
        for field, dtype in self.FIELDS.items():
            first_level, *further_levels = field.split('.')
            value = getattr(listing, first_level, "")
            for level in further_levels:
                if level.isdigit():
                    level = int(level)
                try:
                    value = value[level]
                except Exception:
                    value = ""
                    break

            if "Date" in field:
                # Divide by 1000 because timestamp is in milliseconds
                value = int(value) / 1000

            if dtype:
                value = dtype(field)
            self.data[field.replace('.', '_')] = value
