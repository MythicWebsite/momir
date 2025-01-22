import sys, os, json
import random
import requests
import functools
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGridLayout, QListWidgetItem, QCheckBox
from PySide6.QtGui import QPixmap, QFontDatabase, QFont
from PySide6.QtCore import Qt, QSize, QTimer
from ui_panel import Ui_MainWindow
from ui_loading import Ui_LoadingWindow
from api_handler import find_newest_version, get_creature_card_list, download_img, get_token_list, download_all_images, check_bulk_data, download_json_file
from image_handler import convert_card, flip_card_image
from print_handler import print_card

token_ignore_list = [' Ad', 'Decklist', ' Bio', 'Checklist', 'Punchcard']
token_types = ['token', 'dungeon', 'emblem', 'double_faced_token']
token_card_types = ['Token', 'Card', 'Dungeon', 'Emblem']
card_types = ['Creature', 'Artifact', 'Enchantment', 'Instant', 'Sorcery', 'Planeswalker', 'Land', 'Battle']

display_size = QSize(700,700)

def un_filter(card_list: list, cmc:bool = True) -> list:
    if not cmc:
        return [card for card in card_list if not (card['set_type'] == 'funny' or card['set'] == 'unf') and not card['layout'] in ['token', 'double_faced_token'] and not 'Mystery Booster' in card.get('set_name', '')]
    else:
        for cmc in card_list:
            card_list[cmc] = [card for card in card_list[cmc] if not (card['set_type'] == 'funny' or card['set'] == 'unf') and not card['layout'] in ['token', 'double_faced_token'] and not 'Mystery Booster' in card.get('set_name', '')]
        return card_list


class LoadingWindow(QMainWindow):
    card_data: dict = {}

    def __init__(self):
        super().__init__()
        self.ui = Ui_LoadingWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("Planewalker-38m6.ttf")

        self.show()

        self.set_info("Checking for settings")
        self.set_bar(0)

        if not os.path.exists('json/settings.json'):
            self.card_data['settings'] = {
                'Online': True,
                'Creature': True,
                'Artifact': False,
                'Enchantment': False,
                'Instant': False,
                'Sorcery': False,
                'Planeswalker': False,
                'Land': False,
                'Battle': False,
                'Un': False
            }
            with open('json/settings.json', 'w') as json_file:
                json.dump(self.card_data['settings'], json_file)
        else:
            with open('json/settings.json', 'r') as json_file:
                self.card_data['settings'] = json.load(json_file)

        self.set_info("Checking for preview image")
        self.set_bar(20)

        if not os.path.exists('Images/preview_image.png'):
            convert_card(download_img('https://cards.scryfall.io/border_crop/front/f/5/f5ed5ad3-b970-4720-b23b-308a25f42887.jpg?1562953277'),'preview_image')
        self.set_bar(50)

        if self.card_data['settings']['Online']:
            self.set_info("Checking for updates")
            update = check_bulk_data()
        else:
            update = False

        if update:
            self.set_info("Downloading bulk data")
            with open('json/bulk.json', 'r') as json_file:
                bulk = json.load(json_file)
            for data_type in bulk['data']:
                if data_type['type'] == 'default_cards' or data_type['type'] == 'oracle_cards':
                    self.set_info(f"Downloading {data_type['type']} data from bulk data")
                    self.card_data[data_type['type']] = download_json_file(data_type['download_uri'], f"json/{data_type['type']}.json")
                    self.set_bar(self.ui.progressBar.value() + 25)
        
        self.set_bar(0)
        self.set_info("Reading all unique card data")
        if not self.card_data.get('oracle_cards', None):
            with open('json/oracle_cards.json', 'r', encoding='utf8') as json_file:
                self.card_data['oracle_cards'] = json.load(json_file)
        self.set_bar(20)

        if update:
            self.set_info("Filtering all non-unique card data")
            self.card_data['default_cards'] = [card for card in self.card_data['default_cards'] if 'paper' in card.get('games', []) and not card.get('variation', False) and not card.get('oversized', False) and not card.get('textless', False) and not 'alchemy' == card.get('set_type', '')]
            self.set_bar(50)
            self.set_info("Filtering all unique card data")
            self.card_data['oracle_cards'] = [card for card in self.card_data['oracle_cards'] if any(c in card.get('games', []) for c in ['paper', 'mtgo']) and not card.get('variation', False) and not card.get('oversized', False) and not card.get('textless', False) and not 'alchemy' == card.get('set_type', '')]
            self.set_bar(80)
            self.set_info("Gathering MTGO card data from unique cards")
            mtgo_cards = [card for card in self.card_data['oracle_cards'] if 'mtgo' in card.get('games', False) and not 'paper' in card.get('games', False) or 'Mystery Booster' in card.get('set_name', None)]
            self.set_bar(0)
            self.set_info("Replacing MTGO card data with paper card data")
            total = len(mtgo_cards)
            count = 1
            for card in mtgo_cards:
                card_list = [c for c in self.card_data['default_cards'] if c.get('oracle_id', None) == card['oracle_id'] and 'paper' in c['games'] and not 'Mystery Booster' in c.get('set_name', None)]
                new_card = find_newest_version(card['oracle_id'], card_list)
                if new_card:
                    for i in range(len(self.card_data['oracle_cards'])):
                        if self.card_data['oracle_cards'][i]['oracle_id'] == new_card['oracle_id']:
                            self.card_data['oracle_cards'][i] = new_card
                            break
                count += 1
                if count % int(total/100) == 0:
                    self.set_bar(count/total*100)
            self.set_info("Saving new unique card data")
            self.set_bar(50)
            with open('json/oracle_cards.json', 'w') as json_file:
                json.dump(self.card_data['oracle_cards'], json_file)

            self.set_bar(0)
            self.set_info("Sorting card data")
            for card_type in card_types:
                self.set_info(f"Sorting {card_type} data")
                card_list = [card for card in self.card_data['oracle_cards'] if card_type in card['type_line'].split('//')[0] and not card['layout'] in ['token', 'double_faced_token']]
                card_list = self.sort_data(card_list)
                self.card_data[card_type] = card_list
                with open(f'json/{card_type.lower()}.json', 'w') as json_file:
                    json.dump(card_list, json_file)
                self.set_bar(self.ui.progressBar.value() + 100/len(card_types)+1)
                
            self.set_info("Sorting token data")
            self.card_data['Token'] = [card for card in self.card_data['oracle_cards'] if any(token_type in card['layout'] for token_type in token_types) and not any(ignore in card['name'] for ignore in token_ignore_list) and not card['set_type'] == 'minigame']
            self.card_data['Token'] = sorted(self.card_data['Token'], key=lambda x: x['name'])
            with open('json/token.json', 'w') as json_file:
                json.dump(self.card_data['Token'], json_file)
            self.set_bar(100)
        else:
            self.set_bar(0)
            total = len(card_types) + 1
            count = 1
            for file in os.listdir('json'):
                file_name = file.split('.')[0].capitalize()
                if not file_name.lower() in ['oracle_cards', 'default_cards', 'bulk', 'settings', '']:
                    self.set_info(f"Reading {file_name} data")
                    self.set_bar(count/total*100)
                    count += 1
                    with open(f'json/{file}', 'r') as json_file:
                        self.card_data[file_name] = json.load(json_file)

        # self.set_info("Filtering out tokens from creature data")
        # if all_data:
        #     self.un_creatures = self.card_data['Creature']
        # else:
        #     with open('json/creature.json', 'r') as json_file:
        #         self.un_creatures = json.load(json_file)
        #     with open('json/tokens.json', 'r') as json_file:
        #         self.tokens = json.load(json_file)
        # self.set_bar(50)
        # for cmc in self.un_creatures:
        #     self.creatures[cmc] = [card for card in self.un_creatures[cmc] if not (card['set_type'] == 'funny' or card['set'] == 'unf') and not card['layout'] in ['token', 'double_faced_token'] and not 'Mystery Booster' in card.get('set_name', '')]
        # self.creatures = [card for card in un_creatures if not (card['set_type'] == 'funny' or card['set'] == 'unf')]
        # self.set_bar(70)

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
        self.panel = MainWindow(self.card_data)
        # self.panel.card_data = self.card_data
        all_checks = self.panel.ui.centralwidget.findChildren(QCheckBox)
        for check in all_checks:
            if check.objectName().split('_')[1].capitalize() in self.card_data['settings']:
                check.setChecked(self.card_data['settings'][check.objectName().split('_')[1].capitalize()])
        self.panel.showFullScreen()
        self.close()

class DownloadWindow(QMainWindow):
    def __init__(self, card_data: dict, panel: QMainWindow):
        super().__init__()
        self.ui = Ui_LoadingWindow()
        self.ui.setupUi(self)
        self.set_info("Downloading missing images")
        self.set_bar(0)
        self.panel = panel
        QTimer.singleShot(1000, lambda: self.download_images(card_data))

    def download_images(self, card_data: dict):
        total = len(card_data)
        count = 1
        for current_card in card_data:
            if self.isVisible() is False:
                break
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
                    # print(f"Creating image for {current_card['name']}")
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
            self.set_bar(count/total*100)
        self.panel.debounce = False
        self.close()
        self.panel.showFullScreen()
    
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
    card_data = {}
    
    def __init__(self, card_data: dict):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("Planewalker-38m6.ttf")

        self.card_data = card_data

        all_buttons = self.ui.centralwidget.findChildren(QPushButton)
        all_checks = self.ui.centralwidget.findChildren(QCheckBox)

        for button in all_buttons:
            button.clicked.connect(self.button_animate)
            if button.objectName().split("_")[1].isdigit():
                button.clicked.connect(self.on_cmc_click)
            elif button.objectName().split('_')[1] == 'print':
                button.clicked.connect(self.on_print_click)
            elif button.objectName().split('_')[1] == 'loadtokens':
                button.clicked.connect(self.on_loadtokens_click)
            elif button.objectName().split('_')[0] == 'download':
                button.clicked.connect(self.download_button_click)
            elif button.objectName().split('_')[1] == 'exit':
                button.clicked.connect(self.on_exit_click)

        for check in all_checks:
            check.stateChanged.connect(self.on_check)

        card_back = QPixmap("Images/preview_image.png").scaled(display_size*1.5, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        self.ui.card_display.setPixmap(card_back)
        self.ui.card_display.setAlignment(Qt.AlignCenter)

    def button_animate(self):
        self.sender().setDown(True)
        QApplication.processEvents()
        self.sender().setDown(False)

    def on_exit_click(self):
        self.close()

    def download_button_click(self):
        if not self.debounce:
            self.debounce = True
            card_list = []
            card_type = self.sender().objectName().split('_')[1]
            if card_type not in ["token", "everything"]:
                card_dict = self.card_data[card_type.capitalize()]
                for cmc in card_dict:
                    card_list += card_dict[cmc]
            elif card_type == "token":
                card_list = self.card_data['Token']
            elif card_type == "everything":
                card_list = self.card_data['oracle_cards']
            
            panel = DownloadWindow(card_list, self)
            panel.showNormal()
            self.close()


    def on_cmc_click(self):
        if not self.debounce:
            self.debounce = True
            cmc = self.sender().objectName().split("_")[1]
            choice_list = self.card_data['Creature'] if self.card_data['settings']['Un'] else un_filter(self.card_data['Creature'])
            if not choice_list.get(cmc, None):
                self.debounce = False
                self.logprint(f"No cards of {cmc} CMC exist")
                return
            self.ui.cmc_label.setText(f"CMC: {cmc}")
            found = False
            retry = 0
            while not found and retry < 1000:
                current_card = {'type_line':"no"}
                current_card = random.choice(choice_list[cmc])
                if not current_card:
                    break
                # print(current_card["name"])
                card_loc = None
                if not os.path.exists(f'Images/{current_card["oracle_id"]}.png') and self.card_data['settings']['Online']:
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
                            elif self.card_data['settings']['Online']:
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
            for token in self.card_data['Token']:
                if not any(ignore in token['name'] for ignore in token_ignore_list):
                    card_loc = []
                    img_url = []
                    img_count = 0
                    if not os.path.exists(f'Images/{token["oracle_id"]}.png') and self.card_data['settings']['Online'] and False:
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

    def on_check(self, state):
        if not self.debounce:
            self.debounce = True
            self.setEnabled(False)
            setting = self.sender().objectName().split('_')[1].capitalize()
            # print(f"{setting} box state: ", state)
            self.card_data['settings'][setting] = True if state else False
            with open('json/settings.json', 'w') as json_file:
                json.dump(self.card_data['settings'], json_file)
            self.setEnabled(True)
            self.debounce = False

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