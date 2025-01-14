import requests
import os
import json

api_url = 'https://api.scryfall.com/'

creature_str = '+type%3Acreature'
block_un_str = '+not%3Afunny+-set%3Aunf'

token_searches = ['cards/search?q=layout:token&order=name', 'cards/search?q=layout:emblem&order=name', 'cards/search?q=type:Dungeon&order=name','cards/search?q=layout:double_faced_token+-type:Token+-name:Bounty+-set_type:minigame+-type:Dungeon&order=name']

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
            if not (card.get('all_parts', None) and card.get("mana_cost", "1") == ""):
                if not str(int(card['cmc'])) in creatures:
                    creatures[str(int(card['cmc']))] = []
                creatures[str(int(card['cmc']))].append(card)
    return creatures, next_page, total

def get_creature_card_list(funny: bool = False) -> dict:
    update_check = check_bulk_data()
    path_str = 'json/creatures_no_un.json' if not funny else 'json/creatures_un.json'
    if update_check or not os.path.exists(path_str):
        creatures: dict[list] = {}
        creatures, next_page, total = get_next_creature_page(creatures, api_url + f'cards/search?q=game%3Apaper{creature_str}{block_un_str if not funny else ""}&order=cmc')
        count = 2
        while next_page:
            print(f"Getting next page {count}/{int(total/175+1)}")
            count += 1
            creatures, next_page, total = get_next_creature_page(creatures, next_page)
        save_json_file(creatures, path_str)
        return creatures
    else:
        return load_json_file(path_str)

def get_token_next_page(tokens: list, url: str) -> tuple[dict,str]:
    response = requests.get(url).json()
    if response['has_more']:
        next_page = response['next_page']
    else:
        next_page = None
    total = response['total_cards']
    for token in response['data']:
        if not token['id'] in tokens:
            tokens.append(token)
    return tokens, next_page, total

def get_token_list() -> dict:
    update_check = check_bulk_data()
    if update_check or not os.path.exists('json/tokens.json'):
        tokens: list = []
        for search in token_searches:
            tokens, next_page, total = get_token_next_page(tokens, api_url + search)
            count = 2
            while next_page:
                print(f"Getting next page {count}/{int(total/175+1)}")
                count += 1
                tokens, next_page, total = get_token_next_page(tokens, next_page)
        save_json_file(tokens, 'json/tokens.json')
        return tokens
    else:
        return load_json_file('json/tokens.json')
