import sys, os, json
import random
import requests
import functools
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGridLayout, QListWidgetItem
from PySide6.QtGui import QPixmap, QFontDatabase, QFont
from PySide6.QtCore import Qt, QSize, QTimer
from ui_panel import Ui_MainWindow
from ui_loading import Ui_LoadingWindow
from api_handler import find_newest_version, get_creature_card_list, download_img, get_token_list, download_all_images, check_bulk_data, download_json_file
from image_handler import convert_card, flip_card_image
from print_handler import print_card

test_flip = False
disable_all_tokens = False
offline_mode = True
download_images = False

# if not offline_mode:
#     creatures: dict = get_creature_card_list()
#     un_creatures:dict = get_creature_card_list(funny=True)
#     tokens: list = get_token_list()
# else:
#     with open('json/creatures_no_un.json') as f:
#         creatures = json.load(f)
#     with open('json/creatures_un.json') as f:
#         un_creatures = json.load(f)
#     with open('json/tokens.json') as f:
#         tokens = json.load(f)

# if download_images and not offline_mode:
#     for cmc in un_creatures:
#         download_all_images(un_creatures[cmc], True)
#     download_all_images(tokens)

current_card: dict = {}

token_ignore_list = [' Ad', 'Decklist', ' Bio', 'Checklist', 'Punchcard']
token_types = ['token', 'dungeon', 'emblem', 'double_faced_token']
token_card_types = ['Token', 'Card', 'Dungeon', 'Emblem']
card_types = ['Creature', 'Artifact', 'Enchantment', 'Instant', 'Sorcery', 'Planeswalker', 'Land', 'Battle']

display_size = QSize(700,700)

class LoadingWindow(QMainWindow):
    creatures = {}
    un_creatures = {}
    tokens = []

    def __init__(self):
        super().__init__()
        self.ui = Ui_LoadingWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("Planewalker-38m6.ttf")

        self.show()

        self.set_bar(0)

        if not os.path.exists('Images/preview_image.png'):
            self.ui.loading_info.setText("Downloading preview image")
            self.set_bar(25)
            convert_card(download_img('https://cards.scryfall.io/border_crop/front/f/5/f5ed5ad3-b970-4720-b23b-308a25f42887.jpg?1562953277'),'preview_image')
            self.set_bar(50)
        else:
            self.set_bar(50)

        self.set_info("Checking for updates")
        update = check_bulk_data()
        if update:
            self.set_info("Downloading bulk data")
            with open('json/bulk.json', 'r') as json_file:
                bulk = json.load(json_file)
            for data_type in bulk['data']:
                if data_type['type'] == 'default_cards' or data_type['type'] == 'oracle_cards':
                    self.set_info(f"Downloading {data_type['type']} data from bulk data")
                    download_json_file(data_type['download_uri'], f"json/{data_type['type']}.json")
                    self.set_bar(self.ui.progressBar.value() + 25)
        else:
            self.set_bar(100)
        
        self.set_info("Reading all non-unique card data")
        self.set_bar(0)
        
            
        self.set_info("Reading all unique card data")
        with open('json/oracle_cards.json', 'r', encoding='utf8') as json_file:
            oracle_cards = json.load(json_file)
        self.set_bar(20)
        all_data = {}
        if update:
            with open('json/default_cards.json', 'r', encoding='utf8') as json_file:
                default_cards = json.load(json_file)
            self.set_bar(40)
            self.set_info("Filtering all non-unique card data")
            default_cards = [card for card in default_cards if 'paper' in card.get('games', []) and not card.get('variation', False) and not card.get('oversized', False) and not card.get('textless', False) and not 'alchemy' == card.get('set_type', '')]
            self.set_info("Saving non-unique card data")
            with open('json/default_cards.json', 'w') as json_file:
                json.dump(default_cards, json_file)
            self.set_bar(60)
            self.set_info("Filtering all unique card data")
            oracle_cards = [card for card in oracle_cards if any(c in card.get('games', []) for c in ['paper', 'mtgo']) and not card.get('variation', False) and not card.get('oversized', False) and not card.get('textless', False) and not 'alchemy' == card.get('set_type', '')]
            self.set_bar(80)
            self.set_info("Gathering MTGO card data from unique cards")
            mtgo_cards = [card for card in oracle_cards if 'mtgo' in card.get('games', False) and not 'paper' in card.get('games', False) or 'Mystery Booster' in card.get('set_name', None)]
            self.set_bar(0)
            self.set_info("Replacing MTGO card data with paper card data")
            total = len(mtgo_cards)
            count = 1
            for card in mtgo_cards:
                card_list = [c for c in default_cards if c.get('oracle_id', None) == card['oracle_id'] and 'paper' in c['games'] and not 'Mystery Booster' in c.get('set_name', None)]
                new_card = find_newest_version(card['oracle_id'], card_list)
                if new_card:
                    for i in range(len(oracle_cards)):
                        if oracle_cards[i]['oracle_id'] == new_card['oracle_id']:
                            oracle_cards[i] = new_card
                            break
                count += 1
                if count % int(total/100) == 0:
                    self.set_bar(count/total*100)
            self.set_info("Saving new unique card data")
            with open('json/oracle_cards.json', 'w') as json_file:
                json.dump(oracle_cards, json_file)

            self.set_bar(0)
            self.set_info("Sorting card data")
            for card_type in card_types:
                self.set_info(f"Sorting {card_type} data")
                card_list = [card for card in oracle_cards if card_type in card['type_line'].split('//')[0]]
                card_list = self.sort_data(card_list)
                all_data[card_type] = card_list
                with open(f'json/{card_type.lower()}.json', 'w') as json_file:
                    json.dump(card_list, json_file)
                self.set_bar(self.ui.progressBar.value() + 100/len(card_types)+1)
                
            self.set_info("Sorting token data")
            self.tokens = [card for card in oracle_cards if any(token_type in card['layout'] for token_type in token_types) and not any(ignore in card['name'] for ignore in token_ignore_list) and not card['set_type'] == 'minigame']
            self.tokens = sorted(self.tokens, key=lambda x: x['name'])
            with open('json/tokens.json', 'w') as json_file:
                json.dump(self.tokens, json_file)
            self.set_bar(100)

        self.set_info("Filtering out tokens from creature data")
        if all_data:
            self.un_creatures = all_data['Creature']
        else:
            with open('json/creature.json', 'r') as json_file:
                self.un_creatures = json.load(json_file)
            with open('json/tokens.json', 'r') as json_file:
                self.tokens = json.load(json_file)
        self.set_bar(50)
        for cmc in self.un_creatures:
            self.creatures[cmc] = [card for card in self.un_creatures[cmc] if not (card['set_type'] == 'funny' or card['set'] == 'unf') and not card['layout'] in ['token', 'double_faced_token'] and not 'Mystery Booster' in card.get('set_name', '')]
        # self.creatures = [card for card in un_creatures if not (card['set_type'] == 'funny' or card['set'] == 'unf')]
        self.set_bar(70)

        QApplication.processEvents()
        QTimer.singleShot(1000, self.finished)

    def set_bar(self, value):
        self.ui.progressBar.setValue(value)
        QApplication.processEvents()
    
    def set_info(self, message):
        self.ui.loading_info.setText(message)
        QApplication.processEvents()

    def sort_data(self, card_list):
        cmc_list = {}
        for card in card_list:
            cmc = str(int(card['cmc']))
            if not cmc_list.get(cmc, None):
                cmc_list[cmc] = []
            cmc_list[cmc].append(card)
        return cmc_list

    def finished(self):
        self.panel = MainWindow()
        self.panel.creatures = self.creatures
        self.panel.un_creatures = self.un_creatures
        self.panel.tokens = self.tokens
        self.panel.showFullScreen()
        self.close()

class DownloadWindow(QMainWindow):
    oracle_cards = []

    def __init__(self):
        super().__init__()
        self.ui = Ui_LoadingWindow()
        self.ui.setupUi(self)

        self.set_info("Downloading missing images")
        self.set_bar(0)
        total = len(self.oracle_cards)
        count = 1
        for current_card in self.oracle_cards:
            if not os.path.exists(f'Images/{current_card["oracle_id"]}.png'):
                self.set_info(f"({count}/{total})\nDownloading missing image:\n{current_card['name']}")
                if current_card.get('card_faces', [{}])[0].get('image_uris',None) and "//" in current_card['name']:
                    img_url = current_card['card_faces'][0]['image_uris']['border_crop']
                    img_url2 = current_card['card_faces'][1]['image_uris']['border_crop']
                    if not current_card['layout'] in ['token', 'double_faced_token']:
                        convert_card(flip_card_image(download_img(img_url), download_img(img_url2)), current_card['oracle_id'])
                    else:
                        convert_card(download_img(img_url), current_card['oracle_id'])
                        convert_card(download_img(img_url2), f'{current_card["oracle_id"]}-1')
                else:
                    print(f"Creating image for {current_card['name']}")
                    convert_card(download_img(current_card['image_uris']['border_crop']), current_card['oracle_id'])
                
                if current_card.get('all_parts', None):
                    for part in current_card['all_parts']:
                        if part['component'] == 'token' or any (t_type in part['type_line'] for t_type in token_card_types):
                            if not os.path.exists(f'Images/{part["id"]}.png'):
                                self.set_info(f"({count}/{total})\nDownloading missing image:\n{part['name']}")
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
            count += 1
            if count % int(total/100) == 0:
                self.set_bar(count/total*100)
    
    def set_bar(self, value):
        self.ui.progressBar.setValue(value)
        QApplication.processEvents()
    
    def set_info(self, message):
        self.ui.loading_info.setText(message)
        QApplication.processEvents()

class MainWindow(QMainWindow):
    card_print = None
    token_print = None
    history_print = None
    debounce = False
    creatures = {}
    un_creatures = {}
    tokens = []
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("Planewalker-38m6.ttf")

        all_buttons = self.ui.centralwidget.findChildren(QPushButton)

        for button in all_buttons:
            if button.objectName().split("_")[1].isdigit():
                button.clicked.connect(self.on_cmc_click)
            elif button.objectName().split('_')[1] == 'print':
                button.clicked.connect(self.on_print_click)
            elif button.objectName().split('_')[1] == 'loadtokens':
                button.clicked.connect(self.on_loadtokens_click)

        # self.ui.check_un.stateChanged.connect(self.on_unset_check)

        card_back = QPixmap("Images/preview_image.png").scaled(display_size*1.5, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        self.ui.card_display.setPixmap(card_back)
        self.ui.card_display.setAlignment(Qt.AlignCenter)


    def on_cmc_click(self):
        if not self.debounce:
            self.debounce = True
            cmc = self.sender().objectName().split("_")[1]
            choice_list = self.un_creatures if self.ui.check_un.isChecked() else self.creatures
            if not choice_list.get(cmc, None):
                self.debounce = False
                self.logprint(f"No cards of {cmc} CMC exist")
                return
            self.ui.cmc_label.setText(f"CMC: {cmc}")
            found = False
            retry = 0
            while not found and retry < 1000:
                if not test_flip:
                    current_card = random.choice(choice_list[cmc])
                else:
                    current_card = {'type_line':"no"}
                    stop = 0
                    while not "//" in current_card['type_line'] and stop < 100:
                        current_card = random.choice(choice_list[cmc])
                        stop += 1
                if not current_card:
                    continue
                # print(current_card["name"])
                card_loc = None
                if not os.path.exists(f'Images/{current_card["oracle_id"]}.png') and not offline_mode:
                    # print(f"Creating image for {current_card['name']}")
                    if current_card.get('card_faces', [{}])[0].get('image_uris',None) and "//" in current_card['type_line']:
                        img_url = current_card['card_faces'][0]['image_uris']['border_crop']
                        img_url2 = current_card['card_faces'][1]['image_uris']['border_crop']
                        card_loc = flip_card_image(download_img(img_url), download_img(img_url2))
                        card_loc = convert_card(card_loc, current_card['id'])
                    else:
                        img_url = current_card['image_uris']['border_crop']
                        card_loc = convert_card(download_img(img_url), current_card['id'])
                    found = True
                elif os.path.exists(f'Images/{current_card["oracle_id"]}.png'):
                    card_loc = f'Images/{current_card["oracle_id"]}.png'
                    found = True
                else:
                    retry += 1
                    continue
                if current_card.get('all_parts', None):
                    for part in current_card['all_parts']:
                        if part['component'] == 'token' or any (token_type in part['type_line'] for token_type in token_card_types):
                            token_loc = []
                            if os.path.exists(f'Images/{part["id"]}.png'):
                                token_loc.append(f'Images/{part["id"]}.png')
                                if os.path.exists(f'Images/{part["id"]}-1.png'):
                                    token_loc.append(f'Images/{part["id"]}-1.png')
                            else:
                                card_data = requests.get(part['uri']).json()
                                if card_data.get('image_uris', None):
                                    token_loc.append(convert_card(download_img(card_data['image_uris']['border_crop']), part['id']))
                                elif card_data.get('card_faces', [{}])[0].get('image_uris',None):
                                    face_count = 0
                                    for face in card_data['card_faces']:
                                        if face.get('image_uris', None):
                                            token_loc.append(convert_card(download_img(face['image_uris']['border_crop']), f'{part["id"]}{"-"+str(face_count) if face_count else ""}'))
                                            face_count += 1
                                else:
                                    continue
                            for token in token_loc:
                                self.add_item_to_grid(part, token, self.ui.token_grid)
                                
                self.logprint(f"{current_card['name']} with CMC {cmc} was created")
                self.add_item_to_grid(current_card, card_loc, self.ui.history_grid)

                pixmap = QPixmap(card_loc).scaled(display_size*1.5, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
                self.card_print = card_loc
                self.ui.card_display.setPixmap(pixmap)
                self.ui.card_display.setAlignment(Qt.AlignCenter)
            if not found:
                print("No card found")
            self.debounce = False

    def on_loadtokens_click(self):
        if not self.debounce:
            self.debounce = True
            self.ui.button_loadtokens.setEnabled(False)
            self.ui.button_loadtokens.setText("Loading...")
            QApplication.processEvents()
            self.ui.token_grid_2.takeAt(0).widget().deleteLater()
            count = 0
            for token in self.tokens:
                if not any(ignore in token['name'] for ignore in token_ignore_list):
                    card_loc = []
                    img_url = []
                    img_count = 0
                    if not os.path.exists(f'Images/{token["oracle_id"]}.png') and not True:
                        print(f"Creating image for {token['name']}")
                        if token.get('image_uris', None):
                            img_url.append(token['image_uris']['border_crop'])
                        elif token.get('card_faces', [{}])[0].get('image_uris',None):
                            for face in token['card_faces']:
                                if face.get('image_uris', None):
                                    img_url.append(face['image_uris']['border_crop'])
                        else:
                            continue
                        for img in img_url:
                            card_loc.append(convert_card(download_img(img), f'{token['oracle_id']}{'-'+str(img_count) if img_count else ''}'))
                            img_count += 1
                    elif os.path.exists(f'Images/{token["oracle_id"]}.png'):
                        card_loc.append(f'Images/{token["oracle_id"]}.png')
                        if os.path.exists(f'Images/{token["oracle_id"]}-1.png'):
                            card_loc.append(f'Images/{token["oracle_id"]}-1.png')
                    if card_loc:
                        for cl in card_loc:
                            pixmap = QPixmap(cl).scaled(QSize(250,250), aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
                            new_card = QLabel()
                            new_card.setPixmap(pixmap)
                            new_card.objectName = {cl.split('/')[1].split('.')[0]}
                            self.ui.token_grid_2.addWidget(new_card, count//8, count%8)
                            new_card.mousePressEvent = functools.partial(self.grid_item_click, source_object=new_card)
                            count += 1
            self.debounce = False

    def on_unset_check(self, state):
        print("Check box state: ", state)

    def on_print_click(self):
        if 'card' in self.sender().objectName().split("_")[2]:
            print_card(self.card_print)
        elif 'token' in self.sender().objectName().split("_")[2]:
            print_card(self.token_print)
        elif 'history' in self.sender().objectName().split("_")[2]:
            print_card(self.history_print)

    def add_item_to_grid(self, card: dict, img_loc: str, grid: QGridLayout):
        for i in list(range(grid.count()))[::-1]:
            row, col, _, _ = grid.getItemPosition(i)
            if col == 6:
                row += 1
                col = 0
            else:
                col += 1
            shift_item = grid.itemAt(i).widget()
            grid.addWidget(shift_item, row, col) 
        new_card = QLabel()
        new_card.objectName = {img_loc.split('/')[1].split('.')[0]}
        pixmap_card = QPixmap(img_loc).scaled(QSize(300,300), aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        new_card.setPixmap(pixmap_card)
        new_card.setAlignment(Qt.AlignCenter)
        grid.addWidget(new_card, 0, 0)
        new_card.mousePressEvent = functools.partial(self.grid_item_click, source_object=new_card, grid=grid.objectName().split('_')[0])

    def grid_item_click(self, event, source_object:QLabel = None, grid = 'token'):
        pixmap = QPixmap(f'Images/{str(source_object.objectName).strip('{\'}')}.png').scaled(display_size, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        if grid == 'token':
            self.ui.token_display.setPixmap(pixmap)
            self.ui.token_display_2.setPixmap(pixmap)
            self.ui.token_display.setAlignment(Qt.AlignCenter)
            self.ui.token_display_2.setAlignment(Qt.AlignCenter)
            self.token_print = f'Images/{str(source_object.objectName).strip('{\'}')}.png'
        elif grid == 'history':
            self.ui.history_display.setPixmap(pixmap)
            self.ui.history_display.setAlignment(Qt.AlignCenter)
            self.history_print = f'Images/{str(source_object.objectName).strip('{\'}')}.png'

    def logprint(self, message):
        item = QListWidgetItem(message)
        item.setFont(QFont("SenguiUI"))
        self.ui.action_list.insertItem(0, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Planewalker"))
    window = LoadingWindow()
    # window.show()
    sys.exit(app.exec())