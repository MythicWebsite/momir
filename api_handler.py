import requests
import os
import json
from image_handler import convert_card, flip_card_image
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
    
def download_all_images(data: dict, same_img_flip: bool = False) -> None:
    for current_card in data:
        if not os.path.exists(f'Images/{current_card["id"]}.png'):
            print(f"Downloading {current_card['name']}")
            if current_card.get('card_faces', [{}])[0].get('image_uris',None) and "//" in current_card['type_line']:
                img_url = current_card['card_faces'][0]['image_uris']['border_crop']
                img_url2 = current_card['card_faces'][1]['image_uris']['border_crop']
                if same_img_flip:
                    convert_card(flip_card_image(download_img(img_url), download_img(img_url2)), current_card['id'])
                else:
                    convert_card(download_img(img_url), current_card['id'])
                    convert_card(download_img(img_url2), f'{current_card["id"]}-1')
            else:
                convert_card(download_img(current_card['image_uris']['border_crop']), current_card['id'])
            
            if current_card.get('all_parts', None):
                for part in current_card['all_parts']:
                    if part['component'] == 'token' or any (token_type in part['type_line'] for token_type in token_types):
                        if not os.path.exists(f'Images/{part["id"]}.png'):
                            print(f"Downloading {part['name']}")
                            card_data = requests.get(part['uri']).json()
                            if card_data.get('image_uris', None):
                                convert_card(download_img(card_data['image_uris']['border_crop']), part['id'])
                            elif card_data.get('card_faces', [{}])[0].get('image_uris',None):
                                face_count = 0
                                for face in card_data['card_faces']:
                                    if face.get('image_uris', None):
                                        convert_card(download_img(face['image_uris']['border_crop']), f'{part["id"]}{"-"+str(face_count) if face_count else ""}')
                                        face_count += 1
                            else:
                                continue

def find_newest_version(card_id: str, card_list: list) -> dict:
    newest_card = None
    for card in card_list:
        if card['oracle_id'] == card_id:
            if not newest_card:
                newest_card = card
            elif datetime.strptime(card['released_at'], '%Y-%m-%d') > datetime.strptime(newest_card['released_at'], '%Y-%m-%d'):
                newest_card = card
    return newest_card

def fix_mtgo_cards(oracle_cards: list, default_cards: list, mtgo_cards: list) -> list:
    count = 0
    max_count = len(mtgo_cards)
    print(f'Fixing cards {count}/{max_count}')
    for card in mtgo_cards:
        card_list = [c for c in default_cards if c.get('oracle_id', None) == card['oracle_id'] and 'paper' in c['games']]
        new_card = find_newest_version(card['oracle_id'], card_list)
        if new_card:
            for i in range(len(oracle_cards)):
                if oracle_cards[i]['oracle_id'] == new_card['oracle_id']:
                    oracle_cards[i] = new_card
                    break
        count += 1
        if count % int(max_count/100) == 0:
            print(f'Fixing cards {int(count/max_count*100)}%')
    return oracle_cards

if __name__ == '__main__':
    print('Checking bulk data')
    check_bulk_data()
    print('Opening bulk data')
    with open('json/bulk.json', 'r') as json_file:
        bulk = json.load(json_file)
    print('Checking for default cards')
    if not os.path.exists('json/default_cards.json'):
        for data_type in bulk['data']:
            if data_type['type'] == 'default_cards':
                download_json_file(data_type['download_uri'], 'json/default_cards.json')
                break
    print('Checking for oracle cards')
    if not os.path.exists('json/oracle_cards.json'):
        for data_type in bulk['data']:
            if data_type['type'] == 'oracle_cards':
                download_json_file(data_type['download_uri'], 'json/oracle_cards.json')
                break
    print('Opening default cards')
    with open('json/default_cards.json', 'r', encoding='utf8') as json_file:
        default_cards = json.load(json_file)
    print('Opening oracle cards')
    with open('json/oracle_cards.json', 'r', encoding='utf8') as json_file:
        oracle_cards = json.load(json_file)
    print('Opening no un creatures')
    with open('json/creatures_no_un.json', 'r', encoding='utf8') as json_file:
        no_un_creatures = json.load(json_file)

    print('Filtering oracle cards')
    # oracle_cards = [card for card in oracle_cards if 'Creature' in card.get('type_line', '').split('//')[0] and ('paper' in card.get('games', []) or 'mtgo' in card.get('games', [])) and not card.get('layout', '') == 'token' and not card.get('set_type', '') == 'funny' and not card.get('variation', False) and not card.get('oversized', False) and not card.get('textless', False) and not card.get('security_stamp', '') in ['acorn', 'heart', 'arena', 'circle'] and not card.get('set','') == 'unf']
    oracle_cards = [card for card in oracle_cards if ('paper' in card.get('games', []) or 'mtgo' in card.get('games', [])) and not card.get('variation', False) and not card.get('oversized', False) and not card.get('textless', False)]
    print(len(oracle_cards))
    print('Filtering mtgo cards')
    mtgo_cards = [card for card in oracle_cards if 'mtgo' in card.get('games', False) and not 'paper' in card.get('games', False)]
    print(len(mtgo_cards))
    print('Filtering default cards')
    # default_cards = [card for card in default_cards if 'Creature' in card.get('type_line', '').split('//')[0] and 'paper' in card.get('games', []) and not card.get('layout', '') == 'token' and not card.get('set_type', '') == 'funny' and not card.get('variation', False) and not card.get('oversized', False) and not card.get('textless', False) and not card.get('security_stamp', '') in ['acorn', 'heart', 'arena', 'circle']]
    default_cards = [card for card in default_cards if 'paper' in card.get('games', []) and not card.get('variation', False) and not card.get('oversized', False) and not card.get('textless', False)]
    total = len(mtgo_cards)
    count = 1
    print('Fixing mtgo cards')
    oracle_cards = fix_mtgo_cards(oracle_cards, default_cards, mtgo_cards)

    print(len(oracle_cards))

    