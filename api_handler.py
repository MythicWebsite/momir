import requests
import os
import json

api_url = 'https://api.scryfall.com/'

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
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    return None

def download_json_file(url, file_path) -> None:
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

def download_img(url):
    response = requests.get(url)
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

def get_next_creature_page(creatures, url) -> tuple[dict,str]:
    response = requests.get(url).json()
    if response['has_more']:
        next_page = response['next_page']
    else:
        next_page = None
    total = response['total_cards']
    for card in response['data']:
        if 'Creature' in card['type_line'].split('//')[0]:
            if not str(int(card['cmc'])) in creatures:
                creatures[str(int(card['cmc']))] = []
            creatures[str(int(card['cmc']))].append(card)
    return creatures, next_page, total

def get_creature_card_list() -> dict:
    update_check = check_bulk_data()
    if update_check or not os.path.exists('json/all_creature_cards.json'):
        creatures: dict[list] = {}
        creatures, next_page, total = get_next_creature_page(creatures, api_url + 'cards/search?q=type%3Acreature+game%3Apaper+not%3Afunny+-set%3Aunf&order=cmc')
        count = 2
        while next_page:
            print(f"Getting next page {count}/{int(total/175+1)}")
            count += 1
            creatures, next_page, total = get_next_creature_page(creatures, next_page)
        save_json_file(creatures, 'json/all_creature_cards.json')
        return creatures
    else:
        return load_json_file('json/all_creature_cards.json')
