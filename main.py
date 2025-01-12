from api_handler import get_creature_card_list, download_img
from image_handler import convert_card, flip_card_image
from print_handler import print_card
import random
import os

creatures = get_creature_card_list()
debug_count = 0

while True:
    card = random.choice(creatures['7'])
    if card.get('card_faces', None) and "//" in card['type_line']:
        break

print(f'Selected random {int(card["cmc"])} cmc card: {card["name"]}')
if not os.path.exists(f'Images/{card["id"]}.png'):
    print(f"Creating image for {card['name']}")
    if card.get('card_faces', [{}])[0].get('image_uris',None) and "//" in card['type_line']:
        if not card.get('card_faces', [{}])[1].get('mana_cost',None):
            img_url = card['card_faces'][0]['image_uris']['border_crop']
            img_url2 = card['card_faces'][1]['image_uris']['border_crop']
            card_loc = flip_card_image(download_img(img_url), download_img(img_url2), card['id'])
            card_loc = convert_card(card_loc, card['id'])
        else:
            img_url = card['card_faces'][0]['image_uris']['border_crop']
            card_loc = convert_card(download_img(img_url), card['id'])
    else:
        img_url = card['image_uris']['border_crop']
        card_loc = convert_card(download_img(img_url), card['id'])

    # print_card(card_loc)


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
        