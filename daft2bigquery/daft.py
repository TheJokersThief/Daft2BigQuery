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
        return [
            DaftListing(listing).data
            for listing in 
            self.daft.search(self.options, max_pages=self.max_pages)
        ]


class DaftListing(object):
    FIELDS = [
        'id',
        'title',
        'price',
        'url',
        'sections.0',
        'sections.1',
        'sections.2',
        'featuredLevel',
        'publishDate',
        'category',
        'numBedrooms',
        'numBathrooms',
        'propertyType',
        'media.totalImages',
        'media.hasBrochure',
        'media.hasVirtualTour',
        'ber.rating',
        'description',
        'county.0',
        'area.0',
        'views',
        'point.coordinates.0', # longitude
        'point.coordinates.1', # latitude
    ]
    data = {}
    def __init__(self, listing: Listing):
        for field in self.FIELDS:
            first_level, *further_levels = field.split('.')
            value = getattr(listing, first_level)
            for level in further_levels:
                if level.isdigit():
                    level = int(level)
                value = value[level]
            self.data[field.replace('.', '_')] = value