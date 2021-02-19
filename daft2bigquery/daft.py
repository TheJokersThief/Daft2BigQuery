import time
from daft_scraper.listing import Listing
from daft_scraper.search import DaftSearch, SearchType
from daft_scraper.search.options import SortOption, Sort
from daft_scraper.search.options_location import LocationsOption, Location


class DaftResults():
    def __init__(self, event):
        print("EVENT: ", event)
        self.options = [
            LocationsOption([
                Location(loc)
                for loc in event['locations']
            ])
        ]

        # Always sort by most recent
        self.options.append(SortOption(Sort.MOST_RECENT))
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
        'title': None,
        'price': float,
        'url': None,
        'sections.0': None,
        'sections.1': None,
        'sections.2': None,
        'featuredLevel': None,
        'publishDate': None,
        'category': None,
        'numBedrooms': None,
        'numBathrooms': None,
        'propertyType': None,
        'media.totalImages': None,
        'media.hasBrochure': None,
        'media.hasVirtualTour': None,
        'ber.rating': None,
        'description': None,
        'county.0': None,
        'area.0': None,
        'views': None,
        'point.coordinates.0': float, # longitude
        'point.coordinates.1': float, # latitude
    }
    data = None

    def __init__(self, listing: Listing):
        self.data = {
            'entryDate': int(time.time())
        }
        for field, dtype in self.FIELDS.items():
            first_level, *further_levels = field.split('.')
            
            default = str()
            if dtype:
                default = dtype()
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

            # If any of the fields is empty, we don't want the entry. This happens
            # mostly with prices/numBathrooms for paid sponsor ads
            if value in ["", None]:
                self.data = None
                break

            if dtype:
                # This ensures that things like the price are stored as float even
                # if they're parsed as integers
                value = dtype(value)
            self.data[field.replace('.', '_')] = value
    
