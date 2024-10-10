import googlemaps.maps
import googlemaps.places
from monumentoGooglePlaces.nearby import GooglePlacesNearbySearcher
from monumentoGooglePlaces.utils import write_json
from rich.console import Console
import geopandas as gpd
import googlemaps
from shapely.geometry import mapping
import os
import asyncio
from dotenv import load_dotenv


console = Console()
load_dotenv()

PATH = r'local_data\tl_2024_us_state.zip'
CITIES_SIMPLE_MAP = r'local_data\kx-us-major-cities-SHP.zip'
API_KEY = os.getenv('GOOGLE_MAPS_API')

if __name__ == '__main__':
    df: gpd.GeoDataFrame = gpd.read_file(PATH)
    console.log(df.loc[df['STUSPS'] == 'WA'])
    coords: tuple = mapping(df.iloc[0].geometry).get('coordinates')
    coords = f'{coords[1]},{coords[0]}'
    console.log(coords)

    google_use = False
    if google_use:
        client = googlemaps.Client(key=API_KEY)
        nearby: dict = googlemaps.places.places_nearby(
            client=client,
            location=coords,
            radius=500,
            keyword='Liquour Store',

        )
        console.log(len(nearby.get('results')))

    dev = False
    if dev:
        PLACES = GooglePlacesNearbySearcher(API_KEY)

        task = PLACES.make_search(
            location=coords,
            radius=5000,
            keyword='Liquour Store',
            type_='liquor_store'
        )
        loop = asyncio.new_event_loop()
        res = loop.run_until_complete(task)
        results = res.get('results')
        write_json()
        first_result = res.get('results')[0].get('place_id')
        place = googlemaps.places.place(
            client=googlemaps.Client(key=API_KEY),
            place_id=first_result
        )
        console.log(place)
