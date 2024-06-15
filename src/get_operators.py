from pathlib import Path
import sys
import os
from rich.console import Console
from alive_progress import alive_bar

# XXX Adding the path to get the tools
path = Path(__file__).resolve().parent.parent.parent
sys.path.append(path.__str__())


console = Console()


if __name__ == "__main__":
    from local_backup._01_08_23.mapping import FileMapping
    from TerraDatabase.utils.json_io import write_json, read_json  # noqa
    from google_client.base import GooglePlacesDetailSearcher, GooglePlaceSearcher  # noqa
    from dotenv import load_dotenv

    load_dotenv()

    API_KEY = os.getenv('GOOGLE_MAPS_API')
    searcher = GooglePlaceSearcher(API_KEY)
    details_searcher = GooglePlacesDetailSearcher(API_KEY)

    # Read the fields and blocks geojson files
    blocks_processed = FileMapping.BLOCKS_PROCESSED_2023_08_01_JSON
    fields_processed = FileMapping.FIELDS_ANP_MONGODB_LOG2023_08_01_JSON

    blocks_processed_dicts = read_json(blocks_processed)
    fields_processed_dicts = read_json(fields_processed)

    # Creating a set with the operators from the blocks and fields
    operators = set([d.get("operator") for d in blocks_processed_dicts] + [d.get("operator") for d in fields_processed_dicts])  # noqa
    console.log(f"Operators: {len(operators)}")

    operators_result = []
    operators_not_found = []
    with alive_bar(len(operators)) as bar:
        for operator in operators:

            search = searcher.make_search(operator)
            if search.get('status') == 'OK':
                candidates = search.get('candidates')
                if len(candidates) == 1:
                    candidate = candidates[0]
                    place_id = candidate.get('place_id')
                    details = details_searcher.make_search(place_id)
                    if details.get('status') == 'OK':
                        details = details.get('result')
                        details['operator'] = operator
                        operators_result.append(details)

                if not candidates:
                    operators_not_found.append(operator)

            else:
                console.log(f"Status: {search.get('status')}")
                operators_not_found.append(operator)
            bar()

    write_json('operators.json', operators_result)
    write_json('operators_not_found.json', operators_not_found)
