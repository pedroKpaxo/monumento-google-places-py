from typing import Optional, TypedDict, Dict, Any
import aiohttp
from urllib.parse import quote
from .logger import setup_logger


class NearbySearchParams(TypedDict, total=False):
    """TypedDict for the parameters of the Google Places API nearby search request."""
    keyword: str
    location: str
    radius: int
    type: str
    key: str


class GooglePlacesNearbySearcher:
    """
    Class to search for nearby places using the Google Places API.
    It returns an array of places instead of a single place.
    """
    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    def __init__(self, api_key: str) -> None:
        """
        Initialize the GooglePlacesNearbySearcher with the given API key.

        Args:
            api_key (str): Google Places API key.
        """
        self.api_key = api_key
        self.logger = setup_logger(__class__.__name__)

    def construct_params(
        self,
        location: str,
        radius: int,
        keyword: Optional[str] = None,
        type_: Optional[str] = None
    ) -> NearbySearchParams:
        """
        Construct the parameters for the nearby search request.

        Args:
            location (str): The latitude and longitude of the location, separated by a comma.
            radius (int): The radius in meters within which to search for places.
            keyword (Optional[str]): A term to be matched against place names or types.
            type_ (Optional[str]): Restricts the results to places matching the specified type.

        Returns:
            NearbySearchParams: A dictionary containing the parameters for the request.
        """
        # Properly encode the location parameter

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

    async def make_search(
        self,
        location: str,
        radius: int,
        keyword: Optional[str] = None,
        type_: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform a nearby search using the Google Places API.

        Args:
            location (str): The latitude and longitude of the location, separated by a comma.
            radius (int): The radius in meters within which to search for places.
            keyword (Optional[str]): A term to be matched against place names or types.
            type_ (Optional[str]): Restricts the results to places matching the specified type.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Google Places API.
        """
        params = self.construct_params(location, radius, keyword, type_)
        # Filter out any None values from the params dictionary
        filtered_params = {k: v for k, v in params.items() if v is not None}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.BASE_URL, params=filtered_params) as response:
                    if response.status == 200:
                        self.logger.info(f"Request successful: {response.url}")
                        return await response.json()
                    else:
                        error_message = f"Failed to fetch data: {response.status}, {await response.text()}"
                        self.logger.error(error_message)
                        return {'error': error_message}
            except aiohttp.ClientError as e:
                self.logger.error(f"Request failed: {str(e)}")
                return {'error': 'Request failed'}
