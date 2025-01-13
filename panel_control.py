import sys, os
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QPushButton, QLabel, QCheckBox, QGraphicsScene
from PySide6.QtGui import QPixmap
from ui_panel import Ui_MainWindow
from api_handler import get_creature_card_list, download_img
from image_handler import convert_card, flip_card_image
from print_handler import print_card

creatures = get_creature_card_list()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        all_buttons = self.ui.centralwidget.findChildren(QPushButton)

        for button in all_buttons:
            if button.objectName().split("_")[1].isdigit():
                button.clicked.connect(self.on_cmc_click)

    def on_cmc_click(self):
        cmc = self.sender().objectName().split("_")[1]
        self.ui.cmc_label.setText(f"CMC: {cmc}")
        card = random.choice(creatures[cmc])
        print(card["name"])
        card_loc = None
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
        else:
            card_loc = f'Images/{card["id"]}.png'
        pixmap = QPixmap(card_loc)
        self.ui.card_display.setPixmap(pixmap)

    def on_check(self, state):
        print("Check box state: ", state)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())