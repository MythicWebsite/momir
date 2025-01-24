import requests
import os
import json
import zipfile
import io
from datetime import datetime

api_url = 'https://api.scryfall.com/'

creature_str = '+type%3Acreature'
block_un_str = '+not%3Afunny+-set%3Aunf'

token_searches = ['cards/search?q=layout:token&order=name', 'cards/search?q=layout:emblem&order=name', 'cards/search?q=type:Dungeon&order=name','cards/search?q=layout:double_faced_token+-type:Token+-name:Bounty+-set_type:minigame+-type:Dungeon&order=name']
token_types = ['Token', 'Card', 'Dungeon', 'Emblem']
token_ignore_list = [' Ad', 'Decklist', ' Bio', 'Checklist', 'Punchcard']

def get_card(card_name) -> dict:
    response = requests.get(api_url + 'cards/named?fuzzy=' + card_name)
    card = response.json()
    return card

def get_bulk() -> dict:
    response = requests.get(api_url + 'bulk-data')
    bulk = response.json()
    return bulk

def save_json_file(data, file_path) -> None:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def load_json_file(file_path) -> dict:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf8") as json_file:
            return json.load(json_file)
    return None

def download_json_file(url, file_path) -> None:
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return response.json()

def download_img(url: str, id: str = None):
    response = requests.get(url)
    if id:
        with open(f"Images/{id}.png", 'wb') as file:
            file.write(response.content)
        return f"Images/{id}.png"
    return response.content

def check_bulk_data() -> bool:
    bulk_data = load_json_file('json/bulk.json')
    new_bulk_data = get_bulk()
    if bulk_data != new_bulk_data:
        print('New bulk data available')
        save_json_file(new_bulk_data, 'json/bulk.json')
        return True
    else:
        return False

def find_newest_version(card_id: str, card_list: list) -> dict:
    newest_card = None
    for card in card_list:
        if card['oracle_id'] == card_id:
            if not newest_card:
                newest_card = card
            elif datetime.strptime(card['released_at'], '%Y-%m-%d') > datetime.strptime(newest_card['released_at'], '%Y-%m-%d'):
                newest_card = card
    return newest_card




    