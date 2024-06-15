import json

import requests
from rich.console import Console

console = Console()


def write_json(filename: str, source: list[dict],):
    '''
    Writes a list of dicts to a JSON file.
    Filename = example.json
    Source = list of dictionaries.
    '''
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(source, f, ensure_ascii=False, indent=4)


def get_url(url: str):

    try:
        request = requests.get(url)
        return request

    except Exception as e:
        console.log(e)
        console.log(url)
        return
