import geopandas as gpd
from rich.console import Console

console = Console()

PATH = r'local_data\tl_2024_us_state.zip'
CITIES_SIMPLE_MAP = r'local_data\kx-us-major-cities-SHP.zip'

if __name__ == '__main__':
    df: gpd.GeoDataFrame = gpd.read_file(CITIES_SIMPLE_MAP)
    console.log(df.shape)
    console.log(df)
