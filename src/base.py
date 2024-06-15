import aiohttp
from abc import ABC, abstractmethod
from .logger import setup_logger
from typing import Optional, TypedDict


class AbstractPlaceSearcher(ABC):
    """ Abstract class for a place searcher. """

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.logger = setup_logger(self.__class__.__name__)

    @abstractmethod
    async def make_search(self, query: str) -> dict:
        pass


class NearbySearchParams(TypedDict, total=False):
    """ TypedDict for the parameters of the Google Places API nearby search request."""
    keyword: str
    location: str
    radius: int
    type: str
    key: str


class PlaceSearchParams(TypedDict):
    """ TypedDict for the parameters of the Google Places API search request."""
    input: str
    inputtype: str
    fields: str
    key: str


class PlaceDetailsParams(TypedDict):
    """ TypedDict for the parameters of the Google Places API details request."""
    place_id: str
    fields: str
    key: str


class GooglePlaceSearcher(AbstractPlaceSearcher):
    """
    Class to search for a place using the Google Places API.
    It returns a single place based on the query.
    """

    BASE_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'

    async def make_search(self, query: str) -> dict:
        params: PlaceSearchParams = {
            'input': query,
            'inputtype': 'textquery',
            'fields': 'place_id',
            'key': self.api_key
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status != 200:
                    self.logger.error(f'Error {response.status}: {await response.text()}')
                return await response.json()


class GooglePlacesDetailSearcher(AbstractPlaceSearcher):
    """
    Class to search for details of a place using the Google Places API.
    It returns detailed information about a single place.
    """

    BASE_URL = 'https://maps.googleapis.com/maps/api/place/details/json'

    async def make_search(self, place_id: str) -> dict:
        """Make a request to the Google Places API to get details of a place."""

        params: PlaceDetailsParams = {
            'place_id': place_id,
            'fields': 'name,rating,formatted_phone_number,formatted_address',
            'key': self.api_key
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status != 200:
                    self.logger.error(f'Error {response.status}: {await response.text()}')
                return await response.json()


class GooglePlacesNearbySearcher(AbstractPlaceSearcher):
    """
    Class to search for nearby places using the Google Places API.
    It returns an array of places instead a single place.
    """

    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    def construct_params(self, location: str, radius: int, keyword: Optional[str] = None, type_: Optional[str] = None) -> NearbySearchParams:
        params: NearbySearchParams = {
            'location': location,
            'radius': radius,
            'key': self.api_key
        }
        if keyword:
            params['keyword'] = keyword
        if type_:
            params['type'] = type_
        return params

    async def make_search(self, location: str, radius: int, keyword: Optional[str] = None, type_: Optional[str] = None) -> dict:
        params: NearbySearchParams = {
            'location': location,
            'radius': radius,
            'key': self.api_key
        }
        if keyword:
            params['keyword'] = keyword
        if type_:
            params['type'] = type_

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f'Failed to fetch data: {response.status}, {await response.text()}')
                    return await response.json()
