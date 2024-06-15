import os
import asyncio

import dotenv
from rich.console import Console

from src.base import GooglePlaceSearcher, GooglePlacesDetailSearcher, GooglePlacesNearbySearcher

console = Console()
dotenv.load_dotenv()


async def main():
    API_KEY = os.getenv('GOOGLE_MAPS_API')
    searcher = GooglePlaceSearcher(API_KEY)
    detail_searcher = GooglePlacesDetailSearcher(API_KEY)  # noqa

    # Simultaneously make multiple requests
    task1 = await searcher.make_search("minneapolis liquour store")
    console.log(task1)
    return task1


async def nearby():
    API_KEY = os.getenv('GOOGLE_MAPS_API')
    searcher = GooglePlacesNearbySearcher(API_KEY)

    # Make a search for nearby restaurants around a specific location
    result = await searcher.make_search(location="-33.8670522,151.1957362", radius=1500, keyword="cruise", )
    console.log(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    z = loop.run_until_complete(nearby())
    print(z)
