import sys, os, json
import random
import requests
import functools
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGridLayout, QListWidgetItem
from PySide6.QtGui import QPixmap, QFontDatabase, QFont
from PySide6.QtCore import Qt, QSize
from ui_panel import Ui_MainWindow
from api_handler import get_creature_card_list, download_img, get_token_list, download_all_images
from image_handler import convert_card, flip_card_image
from print_handler import print_card

test_flip = False
disable_all_tokens = False
offline_mode = True
download_images = False

if not offline_mode:
    creatures: dict = get_creature_card_list()
    un_creatures:dict = get_creature_card_list(funny=True)
    tokens: list = get_token_list()
else:
    with open('json/creatures_no_un.json') as f:
        creatures = json.load(f)
    with open('json/creatures_un.json') as f:
        un_creatures = json.load(f)
    with open('json/tokens.json') as f:
        tokens = json.load(f)

if download_images and not offline_mode:
    for cmc in un_creatures:
        download_all_images(un_creatures[cmc], True)
    download_all_images(tokens)

current_card: dict = {}

token_ignore_list = [' Ad', 'Decklist', ' Bio', 'Checklist', 'Punchcard']
token_types = ['Token', 'Card', 'Dungeon', 'Emblem']

display_size = QSize(700,700)

class MainWindow(QMainWindow):
    card_print = None
    token_print = None
    history_print = None
    debounce = False
    
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

        self.ui.check_un.stateChanged.connect(self.on_unset_check)

        if not os.path.exists('Images/preview_image.png'):
            card_back = QPixmap(convert_card(download_img('https://cards.scryfall.io/border_crop/front/f/5/f5ed5ad3-b970-4720-b23b-308a25f42887.jpg?1562953277'),'preview_image')).scaled(display_size*1.5, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        else:
            card_back = QPixmap("Images/preview_image.png").scaled(display_size*1.5, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        self.ui.card_display.setPixmap(card_back)
        self.ui.card_display.setAlignment(Qt.AlignCenter)
        self.ui.token_display.setPixmap(card_back)
        self.ui.token_display.setAlignment(Qt.AlignCenter)
        self.ui.token_display_2.setPixmap(card_back)
        self.ui.token_display_2.setAlignment(Qt.AlignCenter)

        count = 0
        if not disable_all_tokens:
            for token in tokens:
                if not any(ignore in token['name'] for ignore in token_ignore_list):
                    card_loc = []
                    img_url = []
                    img_count = 0
                    if not os.path.exists(f'Images/{token["id"]}.png') and not offline_mode:
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
                            card_loc.append(convert_card(download_img(img), f'{token['id']}{'-'+str(img_count) if img_count else ''}'))
                            img_count += 1
                    elif os.path.exists(f'Images/{token["id"]}.png'):
                        card_loc.append(f'Images/{token["id"]}.png')
                        if os.path.exists(f'Images/{token["id"]}-1.png'):
                            card_loc.append(f'Images/{token["id"]}-1.png')
                    for cl in card_loc:
                        pixmap = QPixmap(cl).scaled(self.ui.tokens_tab_2.size()/1.9, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
                        new_card = QLabel()
                        new_card.setPixmap(pixmap)
                        new_card.objectName = {cl.split('/')[1].split('.')[0]}
                        self.ui.token_grid_2.addWidget(new_card, count//8, count%8)
                        new_card.mousePressEvent = functools.partial(self.grid_item_click, source_object=new_card)
                        count += 1

    def on_cmc_click(self):
        if not self.debounce:
            self.debounce = True
            cmc = self.sender().objectName().split("_")[1]
            choice_list = un_creatures if self.ui.check_un.isChecked() else creatures
            if not choice_list.get(cmc, None):
                self.debounce = False
                self.logprint(f"No cards of {cmc} CMC exist")
                return
            self.ui.cmc_label.setText(f"CMC: {cmc}")
            found = False
            retry = 0
            while not found and retry < 1000:
                if not test_flip:
                    current_card = random.choice(choice_list[cmc]) if self.ui.check_un.isChecked() else random.choice(choice_list[cmc])
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
                if not os.path.exists(f'Images/{current_card["id"]}.png') and not offline_mode:
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
                elif os.path.exists(f'Images/{current_card["id"]}.png'):
                    card_loc = f'Images/{current_card["id"]}.png'
                    found = True
                else:
                    retry += 1
                    continue
                if current_card.get('all_parts', None):
                    for part in current_card['all_parts']:
                        if part['component'] == 'token' or any (token_type in part['type_line'] for token_type in token_types):
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
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())