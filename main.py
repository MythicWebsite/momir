from api_handler import get_creature_card_list, download_img
from image_handler import convert_card
from print_handler import print_card
import random
import os

creatures = get_creature_card_list()
debug_count = 0

card = random.choice(creatures['3'])
print(f'Selected random {int(card["cmc"])} cmc card: {card["name"]}')
if not os.path.exists(f'Images/{card["id"]}.png'):
    print(f"Creating image for {card['name']}")
    img_url = card['image_uris']['border_crop']
    card_loc = convert_card(download_img(img_url), card['id'])
    print_card(card_loc)
# for card in creatures['1']:
#     print(f"Processing {card['name']}")
#     img_url = card['image_uris']['border_crop']
#     convert_card(download_img(img_url), card['id'])
#     debug_count += 1
#     if debug_count >= 10:
#         break
    # if card.get('card_faces', None) and "//" in card['type_line']:
    #     pprint(card["card_faces"], indent=4)
    #     break
        