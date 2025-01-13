import sys, os
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from ui_panel import Ui_MainWindow
from api_handler import get_creature_card_list, download_img
from image_handler import convert_card, flip_card_image
from print_handler import print_card

creatures: dict = get_creature_card_list()
un_creatures:dict = get_creature_card_list(funny=True)
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
        

    def on_cmc_click(self):
        cmc = self.sender().objectName().split("_")[1]
        self.ui.cmc_label.setText(f"CMC: {cmc}")
        current_card = random.choice(un_creatures[cmc]) if self.ui.check_un.isChecked() else random.choice(creatures[cmc])

        print(current_card["name"])
        card_loc = None
        if not os.path.exists(f'Images/{current_card["id"]}.png'):
            print(f"Creating image for {current_card['name']}")
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
        pixmap = QPixmap(card_loc).scaled(self.ui.card_display.size(), aspectMode=Qt.KeepAspectRatio, mode = Qt.SmoothTransformation)
        self.ui.card_display.setPixmap(pixmap)

    def on_unset_check(self, state):
        print("Check box state: ", state)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())