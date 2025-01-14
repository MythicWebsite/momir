import sys, os
import random
import requests
import functools
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from ui_panel import Ui_MainWindow
from api_handler import get_creature_card_list, download_img, get_token_list
from image_handler import convert_card, flip_card_image
from print_handler import print_card

creatures: dict = get_creature_card_list()
un_creatures:dict = get_creature_card_list(funny=True)
tokens: list = get_token_list()
current_card: dict = {}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        all_buttons = self.ui.centralwidget.findChildren(QPushButton)

        for button in all_buttons:
            if button.objectName().split("_")[1].isdigit():
                button.clicked.connect(self.on_cmc_click)

        self.ui.check_un.stateChanged.connect(self.on_unset_check)

        card_back = QPixmap("Magic_card_back.png").scaled(self.ui.card_display.size(), aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        self.ui.card_display.setPixmap(card_back)
        self.ui.token_display.setPixmap(card_back)
        self.ui.token_display_2.setPixmap(card_back)

        count = 0
        for token in tokens:
            if token.get('image_uris', None):
                if not os.path.exists(f'Images/{token["id"]}.png'):
                    print(f"Creating image for {token['name']}")
                    img_url = token['image_uris']['border_crop']
                    card_loc = convert_card(download_img(img_url), token['id'])
                else:
                    card_loc = f'Images/{token["id"]}.png'
                pixmap = QPixmap(card_loc).scaled(self.ui.tokens_tab_2.size()/1.9, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
                new_card = QLabel()
                new_card.setPixmap(pixmap)
                new_card.objectName = {token['id']}
                self.ui.token_grid_2.addWidget(new_card, count//8, count%8)
                new_card.mousePressEvent = functools.partial(self.token_click, source_object=new_card)
                count += 1

    def on_cmc_click(self):
        cmc = self.sender().objectName().split("_")[1]
        self.ui.cmc_label.setText(f"CMC: {cmc}")
        current_card = random.choice(un_creatures[cmc]) if self.ui.check_un.isChecked() else random.choice(creatures[cmc])

        print(current_card["name"])
        card_loc = None
        if not os.path.exists(f'Images/{current_card["id"]}.png'):
            # print(f"Creating image for {current_card['name']}")
            if current_card.get('card_faces', [{}])[0].get('image_uris',None) and "//" in current_card['type_line']:
                if not current_card.get('card_faces', [{}])[1].get('mana_cost',None):
                    img_url = current_card['card_faces'][0]['image_uris']['border_crop']
                    img_url2 = current_card['card_faces'][1]['image_uris']['border_crop']
                    card_loc = flip_card_image(download_img(img_url), download_img(img_url2), current_card['id'])
                    card_loc = convert_card(card_loc, current_card['id'])
                else:
                    img_url = current_card['card_faces'][0]['image_uris']['border_crop']
                    card_loc = convert_card(download_img(img_url), current_card['id'])
            else:
                img_url = current_card['image_uris']['border_crop']
                card_loc = convert_card(download_img(img_url), current_card['id'])
        else:
            card_loc = f'Images/{current_card["id"]}.png'
        if current_card.get('all_parts', None):
            for part in current_card['all_parts']:
                if part['component'] == 'token':
                    if os.path.exists(f'Images/{part["id"]}.png'):
                        token_loc = f'Images/{part["id"]}.png'
                    else:
                        card_data = requests.get(part['uri']).json()
                        token_loc = convert_card(download_img(card_data['image_uris']['border_crop']), part['id'])
                    new_token = QLabel()
                    new_token.objectName = {part['id']}
                    pixmap_token = QPixmap(token_loc).scaled(self.ui.tokens_tab_2.size()/1.9, aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
                    new_token.setPixmap(pixmap_token)
                    self.ui.token_grid.addWidget(new_token, (self.ui.token_grid.count()-8)//8, (self.ui.token_grid.count()-8)%8)
                    new_token.mousePressEvent = functools.partial(self.token_click, source_object=new_token)



        pixmap = QPixmap(card_loc).scaled(self.ui.card_display.size(), aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        self.ui.card_display.setPixmap(pixmap)

    def on_unset_check(self, state):
        print("Check box state: ", state)

    def token_click(self, event, source_object:QLabel = None):
        print(f"Token clicked: {str(source_object.objectName).strip('{\'}')}")
        pixmap = QPixmap(f'Images/{str(source_object.objectName).strip('{\'}')}.png').scaled(self.ui.token_display.size(), aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        self.ui.token_display.setPixmap(pixmap)
        self.ui.token_display_2.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())