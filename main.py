"""
Momir - A Magic: The Gathering card randomizer application.

This application allows users to generate random Magic: The Gathering cards
by converted mana cost (CMC) with various filtering options.
"""

import functools
import json
import os
import random
import sys
import time
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from PySide6.QtCore import Qt, QSize, QTimer, QEventLoop
from PySide6.QtGui import QPixmap, QFontDatabase, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QGridLayout,
    QListWidgetItem, QCheckBox, QAbstractItemView
)

from Data.ui_panel import Ui_MainWindow
from Data.ui_loading import Ui_LoadingWindow
from Data.ui_select import Ui_SelectWindow
from Data.api_handler import find_newest_version, download_img, check_bulk_data, download_json_file, download_images_concurrent, download_double_faced_card_concurrent
from Data.print_handler import print_card

# Application configuration
APP_PATH = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

# Constants for filtering and categorization
TOKEN_IGNORE_LIST = [' Ad', 'Decklist', ' Bio', 'Checklist', 'Punchcard', '// Token']
TOKEN_TYPES = ['token', 'dungeon', 'emblem', 'double_faced_token']
TOKEN_CARD_TYPES = ['Token', 'Card', 'Dungeon', 'Emblem']
CARD_TYPES = ['Creature', 'Artifact', 'Enchantment', 'Instant', 'Sorcery', 'Planeswalker', 'Land', 'Battle']
SET_TYPE_IGNORE = ['alchemy', 'memorabilia', 'vanguard', 'archenemy', 'minigame']

# Display configuration
DISPLAY_SIZE = QSize(700, 700)

# Default application settings
DEFAULT_SETTINGS = {
    'Online': True,
    'Un': False,
    'first_run': True,
    'Select': False,
    'favorites': [],  # List of favorite token oracle_ids
    'type_toggles': {
        'Creature': True,
        'Artifact': False,
        'Enchantment': False,
        'Instant': False,
        'Sorcery': False,
        'Planeswalker': False,
        'Land': False,
        'Battle': False
    }
}

token_progress = 0

def un_filter(card_list: List[Dict[str, Any]], cmc: bool = True) -> List[Dict[str, Any]]:
    """
    Filter out 'Un-' cards (funny/silver-bordered cards) from the card list.
    
    Args:
        card_list: List of card dictionaries or CMC-organized dictionary
        cmc: If True, expects card_list to be organized by CMC
        
    Returns:
        Filtered card list with Un-cards and other unwanted cards removed
    """
    if not cmc:
        return [
            card for card in card_list 
            if not (card['set_type'] == 'funny' or card['set'] == 'unf') 
            and not card['layout'] in ['token', 'double_faced_token'] 
            and not 'Mystery Booster' in card.get('set_name', '')
        ]
    else:
        for cmc_value in card_list:
            card_list[cmc_value] = [
                card for card in card_list[cmc_value] 
                if not (card['set_type'] == 'funny' or card['set'] == 'unf') 
                and not card['layout'] in ['token', 'double_faced_token'] 
                and not 'Mystery Booster' in card.get('set_name', '')
            ]
        return card_list


def get_card_image(card: Dict[str, Any], card_data: Dict[str, Any]) -> Optional[str]:
    """
    Download or retrieve the image for a card.
    
    Args:
        card: Card dictionary with image information
        card_data: Global card data including settings
        
    Returns:
        Path to the card image file, or None if unavailable
    """
    card_loc = None
    image_path = f'Images/{card["oracle_id"]}.png'
    
    if not os.path.exists(image_path) and card_data['settings']['Online']:
        try:
            if card.get('card_faces', [{}])[0].get('image_uris', None) and "//" in card['type_line']:
                img_url = card['card_faces'][0]['image_uris']['border_crop']
                img_url2 = card['card_faces'][1]['image_uris']['border_crop']
                card_loc = download_double_faced_card_concurrent(img_url, img_url2, card['oracle_id'])
            else:
                img_url = card['image_uris']['border_crop']
                card_loc = download_img(img_url, card['oracle_id'])
        except (KeyError, requests.RequestException):
            return None
    elif os.path.exists(image_path):
        card_loc = image_path
        
    return card_loc


def get_related_tokens(card: Dict[str, Any], card_data: Dict[str, Any]) -> List[str]:
    """
    Download or retrieve related token images for a card.
    
    Args:
        card: Card dictionary with token information
        card_data: Global card data including settings
        
    Returns:
        List of paths to token image files
    """
    token_loc = []
    base_path = f'Images/{card["id"]}.png'
    
    if os.path.exists(base_path):
        token_loc.append(base_path)
        if os.path.exists(f'Images/{card["id"]}-1.png'):
            token_loc.append(f'Images/{card["id"]}-1.png')
    elif card_data['settings']['Online']:
        try:
            card_details = requests.get(card['uri']).json()
            
            if card_details.get('image_uris', None):
                token_loc.append(download_img(card_details['image_uris']['border_crop'], card['id']))
            elif card_details.get('card_faces', [{}])[0].get('image_uris', None):
                face_count = 0
                for face in card_details['card_faces']:
                    if face.get('image_uris', None):
                        suffix = f"-{face_count}" if face_count else ""
                        token_loc.append(download_img(
                            face['image_uris']['border_crop'], 
                            f'{card["id"]}{suffix}'
                        ))
                        face_count += 1
        except (KeyError, requests.RequestException):
            pass
            
    return token_loc

class LoadingWindow(QMainWindow):
    """
    Loading window that handles initial data setup and downloading.
    
    This window appears at startup and manages downloading bulk card data,
    filtering cards, and organizing them by type and CMC.
    """
    
    def __init__(self):
        super().__init__()
        self.card_data: Dict[str, Any] = {}
        self.complete: bool = False
        
        self.ui = Ui_LoadingWindow()
        self.ui.setupUi(self)
        self.show()

        self._initialize_directories()
        self._load_settings()
        self._download_preview_image()
        self._process_bulk_data()
        self._finalize_setup()

    def _initialize_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.set_info("Checking for settings")
        self.set_bar(0)

        for directory in ['json', 'Images']:
            if not os.path.exists(directory):
                os.mkdir(directory)

    def _load_settings(self) -> None:
        """Load application settings from file or create default settings."""
        if not os.path.exists('json/settings.json'):
            self.card_data['settings'] = DEFAULT_SETTINGS
            with open('json/settings.json', 'w') as json_file:
                json.dump(self.card_data['settings'], json_file, indent=4)
        else:
            with open('json/settings.json', 'r') as json_file:
                self.card_data['settings'] = json.load(json_file)
            # Ensure all default settings exist
            for setting in DEFAULT_SETTINGS:
                if setting not in self.card_data['settings']:
                    self.card_data['settings'][setting] = DEFAULT_SETTINGS[setting]
        
        if self.card_data['settings']['first_run']:
            if os.path.exists('json/bulk.json'):
                os.remove('json/bulk.json')

    def _download_preview_image(self) -> None:
        """Download the preview image if it doesn't exist."""
        self.set_info("Checking for preview image")
        self.set_bar(20)

        if not os.path.exists('Images/preview_image.png'):
            download_img(
                'https://cards.scryfall.io/border_crop/front/f/5/f5ed5ad3-b970-4720-b23b-308a25f42887.jpg?1562953277',
                'preview_image'
            )
        self.set_bar(50)

    def _process_bulk_data(self) -> None:
        """Process bulk data download and card filtering."""
        if self.card_data['settings']['Online'] or self.card_data['settings']['first_run']:
            self.set_info("Checking for updates")
            update = check_bulk_data()
        else:
            update = False

        if update:
            self._download_and_process_new_data()
        else:
            self._load_existing_data()

    def _download_and_process_new_data(self) -> None:
        """Download and process new bulk data."""
        self.set_info("Downloading bulk data")
        with open('json/bulk.json', 'r') as json_file:
            bulk = json.load(json_file)
            
        for data_type in bulk['data']:
            if data_type['type'] in ['default_cards', 'oracle_cards']:
                self.set_info(f"Downloading {data_type['type']} data from bulk data")
                self.card_data[data_type['type']] = download_json_file(
                    data_type['download_uri'], 
                    f"json/{data_type['type']}.json"
                )
                self.set_bar(self.ui.progressBar.value() + 25)
        
        self._filter_and_organize_cards()

    def _filter_and_organize_cards(self) -> None:
        """Filter and organize downloaded card data."""
        self.set_bar(0)
        self.set_info("Reading all unique card data")
        if not self.card_data.get('oracle_cards', None):
            with open('json/oracle_cards.json', 'r', encoding='utf8') as json_file:
                self.card_data['oracle_cards'] = json.load(json_file)
        self.set_bar(20)

        self.set_info("Filtering card data (optimized)")
        
        ignored_set_types = set(SET_TYPE_IGNORE)
        target_games = {'paper', 'mtgo'}
        
        filtered_default = []
        total_default = len(self.card_data['default_cards'])
        for i, card in enumerate(self.card_data['default_cards']):
            if (card.get('games') and 'paper' in card['games']
                and not card.get('variation', False) 
                and not card.get('oversized', False) 
                and not card.get('textless', False) 
                and card.get('set_type', '') not in ignored_set_types
                and not card.get('full_art', False)):
                filtered_default.append(card)
            
            if i % max(1, total_default // 20) == 0:
                progress = 20 + int((i / total_default) * 15)
                self.set_bar(progress)
                QApplication.processEvents()
        
        self.card_data['default_cards'] = filtered_default
        self.set_bar(35)
        
        self.set_info("Filtering unique card data")
        filtered_oracle = []
        total_oracle = len(self.card_data['oracle_cards'])
        for i, card in enumerate(self.card_data['oracle_cards']):
            card_games = set(card.get('games', []))
            if (card_games & target_games
                and card.get('set_type', '') not in ignored_set_types
                and not (card.get('layout') == 'meld' 
                        and card.get('cmc') 
                        and not card.get('mana_cost'))):
                filtered_oracle.append(card)
            
            if i % max(1, total_oracle // 20) == 0:
                progress = 35 + int((i / total_oracle) * 25)
                self.set_bar(progress)
                QApplication.processEvents()
        
        self.card_data['oracle_cards'] = filtered_oracle
        self.set_bar(80)
        
        self._replace_mtgo_cards()
        self._organize_by_type()

    def _replace_mtgo_cards(self) -> None:
        """Replace MTGO-only cards with their paper equivalents using optimized lookup."""
        self.set_info("Gathering MTGO card data from unique cards")
        mtgo_cards = [
            card for card in self.card_data['oracle_cards'] 
            if 'mtgo' in card.get('games', []) 
            and 'paper' not in card.get('games', [])
            or 'Mystery Booster' in card.get('set_name', '')
        ]
        
        if not mtgo_cards:
            self.set_info("No MTGO-only cards to replace")
            return
        
        self.set_bar(0)
        self.set_info("Building lookup index for faster replacement")
        
        paper_cards_by_oracle = {}
        for card in self.card_data['default_cards']:
            oracle_id = card.get('oracle_id')
            if (oracle_id and 'paper' in card.get('games', []) 
                and 'Mystery Booster' not in card.get('set_name', '')):
                if oracle_id not in paper_cards_by_oracle:
                    paper_cards_by_oracle[oracle_id] = []
                paper_cards_by_oracle[oracle_id].append(card)
        
        self.set_info("Replacing card data with most recent physical versions")
        total = len(mtgo_cards)
        oracle_to_index = {card['oracle_id']: i for i, card in enumerate(self.card_data['oracle_cards'])}
        replacements_made = 0
        
        for count, card in enumerate(mtgo_cards, 1):
            oracle_id = card['oracle_id']
            paper_versions = paper_cards_by_oracle.get(oracle_id, [])
            
            if paper_versions:
                new_card = find_newest_version(oracle_id, paper_versions)
                if new_card:
                    card_index = oracle_to_index.get(oracle_id)
                    if card_index is not None:
                        self.card_data['oracle_cards'][card_index] = new_card
                        replacements_made += 1
            
            if count % max(1, int(total/50)) == 0 or count == total:
                progress = int((count / total) * 50)
                self.set_bar(progress)
                self.set_info(f"Replacing cards: {count}/{total} ({replacements_made} replaced)")
                QApplication.processEvents()
        
        self.set_info(f"Saving updated card data ({replacements_made} cards replaced)")
        self.set_bar(50)
        with open('json/oracle_cards.json', 'w') as json_file:
            json.dump(self.card_data['oracle_cards'], json_file)

    def _organize_by_type(self) -> None:
        """Organize cards by type and save to separate files using optimized processing."""
        self.set_bar(0)
        self.set_info("Organizing card data by type (optimized)")
        
        organized_cards = {card_type: [] for card_type in CARD_TYPES}
        token_cards = []
        
        total_cards = len(self.card_data['oracle_cards'])
        for i, card in enumerate(self.card_data['oracle_cards']):
            type_line = card.get('type_line', '')
            layout = card.get('layout', '')
            card_name = card.get('name', '')
            
            if ((any(token_type in layout for token_type in TOKEN_TYPES) 
                 or 'Dungeon' in type_line)
                and not any(ignore in card_name for ignore in TOKEN_IGNORE_LIST) 
                and card.get('set_type', '') != 'minigame'):
                token_cards.append(card)
            else:
                primary_type_line = type_line.split('//')[0]
                if ('Token' not in primary_type_line 
                    and layout not in ['token', 'double_faced_token']):
                    
                    for card_type in CARD_TYPES:
                        if card_type in primary_type_line:
                            organized_cards[card_type].append(card)
                            breakpoint
            
            if i % max(1, total_cards // 20) == 0:
                progress = int((i / total_cards) * 60)
                self.set_bar(progress)
                self.set_info(f"Categorizing cards: {i}/{total_cards}")
                QApplication.processEvents()
        
        self.set_info("Sorting and organizing card data by CMC")
        
        files_to_write = {}
        for i, card_type in enumerate(CARD_TYPES):
            if organized_cards[card_type]:
                card_list = self.sort_data(organized_cards[card_type])
                self.card_data[card_type] = card_list
                files_to_write[f'json/{card_type.lower()}.json'] = card_list
            else:
                self.card_data[card_type] = {}
                files_to_write[f'json/{card_type.lower()}.json'] = {}
            
            progress = 60 + int(((i + 1) / len(CARD_TYPES)) * 30)
            self.set_bar(progress)
            self.set_info(f"Processing {card_type} data: {len(organized_cards[card_type])} cards")
            QApplication.processEvents()
        
        self.set_info("Processing token data")
        self.card_data['Token'] = sorted(token_cards, key=lambda x: x.get('name', ''))
        files_to_write['json/token.json'] = self.card_data['Token']
        
        self.set_info("Saving all card data files...")
        self.set_bar(95)
        
        
        
        def write_file(file_path_and_data):
            file_path, data = file_path_and_data
            try:
                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file)
                return f"Saved {file_path}"
            except Exception as e:
                return f"Error saving {file_path}: {e}"
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(write_file, files_to_write.items()))
        
        for result in results:
            if "Error" in result:
                print(result)
        
        self.set_bar(100)
        self.set_info(f"Card organization complete! {len(self.card_data['Token'])} tokens, {sum(len(organized_cards[ct]) for ct in CARD_TYPES)} other cards")

    def _load_existing_data(self) -> None:
        """Load existing card data from files using concurrent I/O."""
        self.set_bar(0)
        self.set_info("Loading existing card data (optimized)")
        
        json_files = []
        for file in os.listdir('json'):
            file_name = file.split('.')[0].capitalize()
            if file_name.lower() not in ['oracle_cards', 'default_cards', 'bulk', 'settings', '']:
                json_files.append((file, file_name))
        
        if not json_files:
            self.set_bar(100)
            return
        
        total_files = len(json_files)
        
        def load_json_file(file_info):
            """Load a single JSON file."""
            file, file_name = file_info
            try:
                with open(f'json/{file}', 'r') as json_file:
                    data = json.load(json_file)
                return file_name, data, None
            except Exception as e:
                return file_name, None, str(e)
        
        loaded_count = 0
        with ThreadPoolExecutor(max_workers=min(4, total_files)) as executor:
            future_to_file = {executor.submit(load_json_file, file_info): file_info for file_info in json_files}
            
            for future in as_completed(future_to_file):
                file_info = future_to_file[future]
                loaded_count += 1
                
                try:
                    file_name, data, error = future.result()
                    if error:
                        print(f"Error loading {file_name}: {error}")
                    else:
                        self.card_data[file_name] = data
                        self.set_info(f"Loaded {file_name} data ({len(data) if isinstance(data, list) else 'dict'} items)")
                except Exception as e:
                    print(f"Exception loading {file_info[1]}: {e}")
                
                progress = int((loaded_count / total_files) * 100)
                self.set_bar(progress)
                QApplication.processEvents()
        
        self.set_info(f"Loaded {loaded_count} card data files")
        self.set_bar(100)

    def _finalize_setup(self) -> None:
        """Finalize the setup and transition to main window."""
        self.card_data['settings']['first_run'] = False
        self.complete = True
        
        with open('json/settings.json', 'w') as json_file:
            json.dump(self.card_data['settings'], json_file, indent=4)
        
        QApplication.processEvents()
        QTimer.singleShot(1000, self.finished)

    def closeEvent(self, event) -> None:
        """Handle window close event - exit if loading is not complete."""
        if not self.complete:
            sys.exit()

    def set_bar(self, value: int) -> None:
        """
        Update the progress bar value.
        
        Args:
            value: Progress percentage (0-100)
        """
        self.ui.progressBar.setValue(int(value))
        QApplication.processEvents()
    
    def set_info(self, message: str) -> None:
        """
        Update the loading information text.
        
        Args:
            message: Information message to display
        """
        self.ui.loading_info.setText(message)
        QApplication.processEvents()

    def sort_data(self, card_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Sort cards by converted mana cost (CMC).
        
        Args:
            card_list: List of card dictionaries
            
        Returns:
            Dictionary with CMC as keys and card lists as values
        """
        cmc_list = {}
        for card in card_list:
            cmc = str(int(card.get('cmc', 0)))
            if cmc not in cmc_list:
                cmc_list[cmc] = []
            cmc_list[cmc].append(card)
        return cmc_list

    def finished(self) -> None:
        """Initialize the main panel and close the loading window."""
        try:
            self.panel = MainWindow(self.card_data)
            
            all_checks = self.panel.ui.centralwidget.findChildren(QCheckBox)
            for check in all_checks:
                check_name = check.objectName().split('_')[1].capitalize()
                if check_name in self.card_data['settings']['type_toggles']:
                    check.setChecked(self.card_data['settings']['type_toggles'][check_name])
                elif check_name in self.card_data['settings']:
                    check.setChecked(self.card_data['settings'][check_name])
            
            self.panel.debounce = False
            self.panel.setup_cur_data()
            self.panel.showFullScreen()
            self.deleteLater()
        except Exception as e:
            print(f"Error initializing main window: {e}")
            sys.exit(1)

class DownloadWindow(QMainWindow):
    """
    Window for downloading missing card images in batch.
    
    This window appears when the user requests to download images
    and shows progress of the download operation.
    """
    
    def __init__(self, card_data: List[Dict[str, Any]], panel: QMainWindow):
        super().__init__()
        self.ui = Ui_LoadingWindow()
        self.ui.setupUi(self)
        
        self.set_info("Downloading missing images")
        self.set_bar(0)
        self.panel = panel
        
        self.safety_timer = QTimer()
        self.safety_timer.timeout.connect(self._safety_restore_panel)
        self.safety_timer.setSingleShot(True)
        self.safety_timer.start(300000)
        
        QTimer.singleShot(1000, lambda: self.download_images(card_data))

    def download_images(self, card_data: List[Dict[str, Any]]) -> None:
        """
        Download missing images for the provided card data using concurrent downloads.
        
        Args:
            card_data: List of card dictionaries to download images for
        """
        if not self.panel.card_data['settings']['Online']:
            self.set_info("Online mode is disabled. Cannot download images.")
            QTimer.singleShot(2000, self._finish_download)
            return
            
        download_tasks = []
        double_faced_tasks = []
        token_parts = []
        
        self.set_info("Preparing download list...")
        total_cards = len(card_data)
        
        for idx, current_card in enumerate(card_data):
            if not self.isVisible():
                break
                
            if idx % max(1, total_cards // 20) == 0:
                prep_progress = int((idx / total_cards) * 30)
                self.set_bar(prep_progress)
                self.set_info(f"Preparing download list... ({idx}/{total_cards})")
                QApplication.processEvents()
                
            try:
                image_path = f'Images/{current_card["oracle_id"]}.png'
                if not os.path.exists(image_path):
                    if (current_card.get('card_faces', [{}])[0].get('image_uris', None) and 
                        "//" in current_card['type_line']) and not "// Token" in current_card['type_line']:
                        try:
                            front_url = current_card['card_faces'][0]['image_uris']['border_crop']
                            back_url = current_card['card_faces'][1]['image_uris']['border_crop']
                            double_faced_tasks.append((front_url, back_url, current_card['oracle_id']))
                        except (KeyError, IndexError):
                            continue
                    else:
                        card_url = self._get_card_image_url(current_card)
                        if card_url:
                            download_tasks.append((card_url, image_path))
                    
                    if current_card.get('all_parts', None):
                        for part in current_card['all_parts']:
                            if (part['component'] in ['token', 'meld_result'] or 
                                any(token_type in part['type_line'] for token_type in TOKEN_CARD_TYPES)):
                                token_parts.append(part)
                                
            except Exception as e:
                print(f"Error preparing download for {current_card.get('name', 'unknown card')}: {e}")
                continue
        
        self.set_info("Processing token requirements...")
        self.set_bar(30)
        QApplication.processEvents()
        
        for part in token_parts:
            if not self.isVisible():
                break
            base_path = f'Images/{part["id"]}.png'
            if not os.path.exists(base_path):
                download_tasks.append(('TOKEN_URI:' + part['uri'], base_path))
        
        if not download_tasks and not double_faced_tasks:
            self.set_info("No images to download!")
            self.set_bar(100)
            self._finish_download()
            return
            
        total_tasks = len(download_tasks) + len(double_faced_tasks)
        self.set_info(f"Starting download of {total_tasks} images...")
        self.set_bar(35)
        
        self._process_concurrent_downloads(download_tasks, double_faced_tasks)
    
    def _process_concurrent_downloads(self, download_tasks: List[tuple[str, str]], double_faced_tasks: List[tuple[str, str, str]]) -> None:
        """Process all downloads concurrently with proper progress tracking."""
        total_count = len(download_tasks) + len(double_faced_tasks)
        completed_count = 0
        successful_downloads = []
        failed_downloads = []
        
        try:
            regular_tasks = [(url, path) for url, path in download_tasks if not url.startswith('TOKEN_URI:')]
            token_uri_tasks = [(url[10:], path) for url, path in download_tasks if url.startswith('TOKEN_URI:')]  # Remove 'TOKEN_URI:' prefix
            
            if regular_tasks:
                def regular_progress_callback(completed: int, total: int, current_file: str):
                    nonlocal completed_count
                    actual_completed = completed_count + completed
                    if self.isVisible():
                        progress = 35 + int((actual_completed / total_count) * 60)  # Use 35-95% for downloads
                        self.set_bar(progress)
                        self.set_info(f"Downloading images: {actual_completed}/{total_count}\nCurrent: {current_file}")
                
                regular_successful, regular_failed = download_images_concurrent(
                    regular_tasks, 
                    progress_callback=regular_progress_callback,
                    max_workers=8
                )
                successful_downloads.extend(regular_successful)
                failed_downloads.extend(regular_failed)
                completed_count += len(regular_tasks)
            
            if token_uri_tasks:
                self.set_info(f"Processing {len(token_uri_tasks)} token URIs...")
                
                def process_token_uri(token_uri_and_path):
                    """Process a single token URI and return download tasks."""
                    token_uri, base_path = token_uri_and_path
                    token_download_tasks = []
                    
                    try:
                        token_data = requests.get(token_uri, timeout=30).json()
                        
                        if token_data.get('image_uris', None):
                            token_download_tasks.append((token_data['image_uris']['border_crop'], base_path))
                        elif token_data.get('card_faces', [{}])[0].get('image_uris', None):
                            for face_count, face in enumerate(token_data['card_faces']):
                                if face.get('image_uris', None):
                                    suffix = f"-{face_count}" if face_count else ""
                                    face_path = f'Images/{os.path.basename(base_path).split(".")[0]}{suffix}.png'
                                    if not os.path.exists(face_path):
                                        token_download_tasks.append((face['image_uris']['border_crop'], face_path))
                        
                        return token_download_tasks, None
                        
                    except requests.RequestException as e:
                        return [], (base_path, f"Token fetch failed: {str(e)}")
                
                all_token_download_tasks = []
                token_processing_failed = []
                
                with ThreadPoolExecutor(max_workers=min(8, len(token_uri_tasks))) as executor:
                    future_to_token = {
                        executor.submit(process_token_uri, token_task): token_task
                        for token_task in token_uri_tasks
                    }
                    
                    processed_tokens = 0
                    
                    for future in as_completed(future_to_token):
                        if not self.isVisible():
                            break
                            
                        token_uri, base_path = future_to_token[future]
                        processed_tokens += 1
                        
                        try:
                            token_tasks, error = future.result()
                            if error:
                                token_processing_failed.append(error)
                            else:
                                all_token_download_tasks.extend(token_tasks)
                                
                        except Exception as e:
                            token_processing_failed.append((base_path, f"Token processing exception: {str(e)}"))
                        
                        if self.isVisible():
                            progress = 35 + int(((completed_count + processed_tokens) / total_count) * 30) 
                            self.set_bar(progress)
                            self.set_info(f"Processing tokens: {processed_tokens}/{len(token_uri_tasks)}")
                
                if all_token_download_tasks:
                    self.set_info(f"Downloading {len(all_token_download_tasks)} token images...")
                    
                    def token_download_progress(completed: int, total: int, current_file: str):
                        if self.isVisible():
                            base_progress = 35 + int(((completed_count + len(token_uri_tasks)) / total_count) * 30)
                            additional_progress = int((completed / total) * 20)
                            progress = base_progress + additional_progress
                            self.set_bar(min(progress, 90))
                            self.set_info(f"Downloading token images: {completed}/{total}\nCurrent: {current_file}")
                    
                    token_successful, token_failed = download_images_concurrent(
                        all_token_download_tasks,
                        progress_callback=token_download_progress,
                        max_workers=8
                    )
                    successful_downloads.extend(token_successful)
                    failed_downloads.extend(token_failed)
                
                failed_downloads.extend(token_processing_failed)
                completed_count += len(token_uri_tasks)
            
            if double_faced_tasks:
                self.set_info(f"Processing {len(double_faced_tasks)} double-faced cards...")
                
                def process_double_faced_card(df_task):
                    """Process a single double-faced card."""
                    front_url, back_url, oracle_id = df_task
                    result = download_double_faced_card_concurrent(front_url, back_url, oracle_id)
                    return result, oracle_id
                
                with ThreadPoolExecutor(max_workers=min(4, len(double_faced_tasks))) as executor:
                    future_to_df = {
                        executor.submit(process_double_faced_card, df_task): df_task
                        for df_task in double_faced_tasks
                    }
                    
                    processed_df = 0
                    
                    for future in as_completed(future_to_df):
                        if not self.isVisible():
                            break
                            
                        df_task = future_to_df[future]
                        processed_df += 1
                        
                        try:
                            result, oracle_id = future.result()
                            if result:
                                successful_downloads.append(result)
                            else:
                                failed_downloads.append((f"Images/{oracle_id}.png", "Double-faced card combination failed"))
                                
                        except Exception as e:
                            oracle_id = df_task[2]
                            failed_downloads.append((f"Images/{oracle_id}.png", f"Double-faced processing exception: {str(e)}"))
                        
                        if self.isVisible():
                            progress = 85 + int((processed_df / len(double_faced_tasks)) * 10)  # Use final 10% for double-faced
                            self.set_bar(progress)
                            self.set_info(f"Processing double-faced cards: {processed_df}/{len(double_faced_tasks)}")
                
                completed_count += len(double_faced_tasks)
            
            if self.isVisible():
                self.set_bar(95)
                self.set_info(f"Download complete!\nSuccessful: {len(successful_downloads)}\nFailed: {len(failed_downloads)}")
                if failed_downloads:
                    print(f"Failed downloads: {len(failed_downloads)}")
                    for file_path, error in failed_downloads:
                        print(f"  {file_path}: {error}")
                        
                self._finish_download()
                
        except Exception as e:
            print(f"Error during concurrent download: {e}")
            self.set_info(f"Download error: {str(e)}")
            self._finish_download()
    
    def _get_card_image_url(self, card: Dict[str, Any]) -> Optional[str]:
        """Extract the image URL from a card dictionary (for single-faced cards only)."""
        try:
            return card['image_uris']['border_crop']
        except KeyError:
            return None
    
    def _finish_download(self) -> None:
        """Finish the download process and return to main panel."""
        try:
            if not self.panel:
                print("CRITICAL ERROR: Panel reference is None!")
                self.set_info("CRITICAL ERROR: Lost main window reference!")
                return
            
            self.panel.restore_from_download()
            
            for _ in range(5):
                QApplication.processEvents()
            
            if not self.panel.isVisible():
                self.panel.show()
                self.panel.showNormal()
                self.panel.showFullScreen()
                self.panel.raise_()
                self.panel.activateWindow()
                QApplication.processEvents()
            
            final_check_attempts = 0
            while not self.panel.isVisible() and final_check_attempts < 20:
                self.panel.showFullScreen()
                self.panel.raise_()
                self.panel.activateWindow()
                QApplication.processEvents()
                final_check_attempts += 1
                
                time.sleep(0.1)
            
            if self.panel.isVisible():
                super().close()
            else:
                self.set_info("ERROR: Could not restore main window!\nPlease manually close this window and restart the application.")
                
        except Exception as e:
            print(f"EXCEPTION in _finish_download: {e}")
            
            try:
                if self.panel:
                    self.panel.showFullScreen()
                    self.panel.raise_()
                    self.panel.activateWindow()
                    QApplication.processEvents()
                    
                    if self.panel.isVisible():
                        super().close()
                    else:
                        self.set_info("EMERGENCY: Main window restoration failed!")
            except Exception as e2:
                print(f"Emergency restoration also failed: {e2}")
                self.set_info("CRITICAL FAILURE: Application may need to be restarted")
    
    def _safety_restore_panel(self) -> None:
        """Safety method to restore main panel if download takes too long or fails."""
        try:
            if self.panel:
                self.panel.restore_from_download()
            
            if self.isVisible():
                self.close()
        except Exception as e:
            print(f"Error in safety restore: {e}")
    
    def closeEvent(self, event) -> None:
        """Handle window close event - restore main panel if download window is closed."""
        try:
            if self.panel:
                self.panel.restore_from_download()
        except Exception as e:
            print(f"Error in closeEvent: {e}")
            if self.panel:
                try:
                    self.panel.restore_from_download()
                except Exception as e2:
                    print(f"Fallback closeEvent restoration failed: {e2}")
        
        event.accept()
    
    def set_bar(self, value: int) -> None:
        """Update progress bar value."""
        self.ui.progressBar.setValue(int(value))
        QApplication.processEvents()
    
    def set_info(self, message: str) -> None:
        """Update information text."""
        self.ui.loading_info.setText(message)
        QApplication.processEvents()


class SelectWindow(QMainWindow):
    """
    Window for selecting from multiple card options.
    
    This window appears when the 'Select' mode is enabled and shows
    multiple card options for the user to choose from.
    """
    
    def __init__(self, card_list: List[Dict[str, Any]], card_locs: List[str], panel: QMainWindow):
        super().__init__()
        self.debounce: bool = False
        
        self.ui = Ui_SelectWindow()
        self.ui.setupUi(self)
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.card_list = card_list
        self.panel = panel

        self._setup_card_displays(card_locs)

    def _setup_card_displays(self, card_locs: List[str]) -> None:
        """
        Set up the card display labels with images.
        
        Args:
            card_locs: List of image file paths
        """
        labels = self.ui.centralwidget.findChildren(QLabel)
        for label in labels:
            if 'card_' in label.objectName():
                try:
                    card_no = int(label.objectName().strip('card_')) - 1
                    if card_no < len(card_locs):
                        pixmap = QPixmap(card_locs[card_no]).scaled(
                            QSize(1000, 1000), 
                            aspectMode=Qt.KeepAspectRatio, 
                            mode=Qt.SmoothTransformation
                        )
                        label.setPixmap(pixmap)
                        label.setAlignment(Qt.AlignCenter)
                        label.mousePressEvent = functools.partial(self.on_card_click, source_object=label)
                except (ValueError, IndexError) as e:
                    print(f"Error setting up card display {label.objectName()}: {e}")

    def on_card_click(self, event, source_object: QLabel = None) -> None:
        """
        Handle card selection click.
        
        Args:
            event: Mouse click event
            source_object: The label that was clicked
        """
        if not self.debounce and source_object:
            try:
                self.debounce = True
                card_index = int(source_object.objectName().strip('card_')) - 1
                if 0 <= card_index < len(self.card_list):
                    self.panel.selected_card = self.card_list[card_index]
                self.panel.debounce = False
                self.deleteLater()
            except (ValueError, IndexError) as e:
                print(f"Error handling card click: {e}")
                self.debounce = False

class MainWindow(QMainWindow):
    card_print = None
    token_print = None
    history_print = None
    debounce = True
    card_data = {}
    selected_card = None
    selected_token_id = None  # Track currently selected token for favoriting
    
    def __init__(self, card_data: dict):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.card_data = card_data

        all_buttons = self.ui.centralwidget.findChildren(QPushButton)
        all_checks = self.ui.centralwidget.findChildren(QCheckBox)

        self.ui.action_list.setDragDropMode(QAbstractItemView.NoDragDrop)

        for button in all_buttons:
            button.clicked.connect(self.button_animate)
            if button.objectName().split("_")[1].isdigit():
                button.clicked.connect(self.on_cmc_click)
            elif button.objectName().split('_')[1] == 'print':
                button.clicked.connect(self.on_print_click)
            elif button.objectName().split('_')[1] == 'loadtokens':
                button.clicked.connect(self.on_loadtokens_click)
            elif button.objectName().split('_')[1] == 'favorite':
                button.clicked.connect(self.on_favorite_click)
            elif button.objectName().split('_')[0] == 'download':
                button.clicked.connect(self.download_button_click)
            elif button.objectName().split('_')[1] == 'exit':
                button.clicked.connect(self.on_exit_click)

        for check in all_checks:
            check.stateChanged.connect(self.on_check)

        card_back = self._create_scaled_pixmap("Images/preview_image.png", DISPLAY_SIZE*1.5)
        self.ui.card_display.setPixmap(card_back)
        self.ui.card_display.setAlignment(Qt.AlignCenter)
        
        # Initialize favorite button text
        self.ui.button_favorite_token.setText("Favorite")

    def _create_scaled_pixmap(self, image_path: str, size: QSize) -> QPixmap:
        """Create a scaled pixmap with consistent parameters."""
        return QPixmap(image_path).scaled(
            size, 
            aspectMode=Qt.KeepAspectRatio, 
            mode=Qt.SmoothTransformation
        )

    def button_animate(self):
        self.sender().setDown(True)
        QApplication.processEvents()
        self.sender().setDown(False)

    def on_exit_click(self):
        self.close()

    def on_favorite_click(self):
        """Toggle favorite status of currently selected token."""
        if not self.selected_token_id:
            # No token selected, update button text to indicate this
            self.ui.button_favorite_token.setText("Select a token first")
            QTimer.singleShot(2000, lambda: self.ui.button_favorite_token.setText("Favorite"))
            return
        
        if 'favorites' not in self.card_data['settings']:
            self.card_data['settings']['favorites'] = []
        
        favorites = self.card_data['settings']['favorites']
        
        if self.selected_token_id in favorites:
            # Remove from favorites
            favorites.remove(self.selected_token_id)
            self.ui.button_favorite_token.setText("Favorite")
        else:
            # Add to favorites
            favorites.append(self.selected_token_id)
            self.ui.button_favorite_token.setText("❤️ Unfavorite")
        
        # Save settings
        self._save_settings()
        
        # Refresh the token grid to show new order immediately
        self._refresh_token_grid()
        
        # Update button text back to normal after a moment
        QTimer.singleShot(1500, self._update_favorite_button_text)

    def _save_settings(self):
        """Save current settings to file."""
        try:
            with open('json/settings.json', 'w') as json_file:
                json.dump(self.card_data['settings'], json_file, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def _update_favorite_button_text(self):
        """Update favorite button text based on current selection."""
        if not self.selected_token_id:
            self.ui.button_favorite_token.setText("Favorite")
        elif self.selected_token_id in self.card_data['settings'].get('favorites', []):
            self.ui.button_favorite_token.setText("❤️ Unfavorite")
        else:
            self.ui.button_favorite_token.setText("Favorite")

    def _refresh_token_grid(self):
        """Refresh the token grid to reflect new favorite order."""
        # Check if tokens are currently loaded
        if self.ui.token_grid_2.count() == 0:
            return  # No tokens loaded, nothing to refresh
        
        # Store current grid state
        current_widgets = []
        for i in range(self.ui.token_grid_2.count()):
            item = self.ui.token_grid_2.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                token_id = str(widget.objectName).strip('{\'}')
                current_widgets.append({
                    'widget': widget,
                    'token_id': token_id,
                    'pixmap': widget.pixmap()
                })
        
        # Clear the grid
        while self.ui.token_grid_2.count():
            child = self.ui.token_grid_2.takeAt(0)
            if child.widget():
                child.widget().setParent(None)  # Don't delete, just remove from layout
        
        # Sort widgets: favorites first, then regular
        favorites = self.card_data['settings'].get('favorites', [])
        favorite_widgets = [w for w in current_widgets if w['token_id'] in favorites]
        regular_widgets = [w for w in current_widgets if w['token_id'] not in favorites]
        sorted_widgets = favorite_widgets + regular_widgets
        
        # Re-add widgets to grid in new order
        for i, widget_data in enumerate(sorted_widgets):
            widget = widget_data['widget']
            
            # Update visual styling for favorites
            if widget_data['token_id'] in favorites:
                widget.setStyleSheet("border: 3px solid gold; border-radius: 5px;")
                widget.setToolTip("Favorite")
            else:
                widget.setStyleSheet("")
                widget.setToolTip("")
            
            # Calculate grid position
            row = i // 8
            col = i % 8
            
            self.ui.token_grid_2.addWidget(widget, row, col)
        
        QApplication.processEvents()

    def setup_cur_data(self):
        self.card_data['cur_data'] = {}
        for setting in self.card_data['settings']['type_toggles']:
            if self.card_data['settings']['type_toggles'][setting]:
                for cmc in set(self.card_data[setting].keys()).union(self.card_data['cur_data'].keys()):
                    self.card_data['cur_data'][cmc] = self.card_data[setting].get(cmc, []) + self.card_data['cur_data'].get(cmc, [])
        if not self.card_data['settings']['Un']:
            self.card_data['cur_data'] = un_filter(self.card_data['cur_data'])

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
            
            self.stored_window_state = {
                'was_fullscreen': self.isFullScreen(),
                'was_maximized': self.isMaximized(),
                'window_state': self.windowState(),
                'geometry': self.geometry()
            }
            
            self.hide()
            download_window = DownloadWindow(card_list, self)
            download_window.showNormal()
    
    def restore_from_download(self):
        """Restore the main window after download completion."""
        try:
            self.debounce = False
            QApplication.processEvents()
            
            stored_state = getattr(self, 'stored_window_state', {})
            
            if self.isHidden():
                self.show()
                QApplication.processEvents()
            
            if stored_state.get('was_fullscreen', True):
                self.showFullScreen()
            elif stored_state.get('was_maximized', False):
                self.showMaximized()
            else:
                self.showNormal()
                if 'geometry' in stored_state:
                    self.setGeometry(stored_state['geometry'])
            
            QApplication.processEvents()
            self.raise_()
            self.activateWindow()
            QApplication.processEvents()
            
        except Exception as e:
            print(f"EXCEPTION in restore_from_download: {e}")
            
            try:
                self.debounce = False
                self.show()
                self.showFullScreen()
                self.raise_()
                self.activateWindow()
                QApplication.processEvents()
            except Exception as e2:
                print(f"Fallback restoration also failed: {e2}")

    def on_cmc_click(self):
        if not self.debounce:
            self.debounce = True
            cmc = self.sender().objectName().split("_")[1]
            choice_list = self.card_data['cur_data']
            if not choice_list.get(cmc, None):
                self.debounce = False
                self.logprint(f"No cards of {cmc} CMC exist")
                return
            self.ui.cmc_label.setText(f"CMC: {cmc}")
            found = False
            retry = 0
            while not found and retry < 1000:
                if not len(choice_list[cmc]):
                    break
                if self.card_data['settings']['Select']:
                    choices = []
                    card_locs = []
                    attempts = 0
                    while len(choices) < 3:
                        card = random.choice(choice_list[cmc])
                        if not card in choices or attempts > 99:
                            loc = get_card_image(card, self.card_data)
                            if loc:
                                choices.append(card)
                                card_locs.append(loc)
                        if attempts > 999:
                            break
                        attempts += 1
                    select_window = SelectWindow(choices, card_locs, self)
                    select_window.showFullScreen()
                    loop = QEventLoop()
                    select_window.destroyed.connect(loop.quit)
                    loop.exec()
                    if not self.selected_card:
                        break
                    current_card = self.selected_card
                else:
                    current_card = random.choice(choice_list[cmc])
                card_loc = get_card_image(current_card, self.card_data)
                if not card_loc:
                    retry += 1
                    continue
                found = True
                if current_card.get('all_parts', None):
                    for part in current_card['all_parts']:
                        if part['component'] in ['token','meld_result'] or any (token_type in part['type_line'] for token_type in TOKEN_CARD_TYPES):
                            token_loc = get_related_tokens(part, self.card_data)
                            for token in token_loc:
                                self.add_item_to_grid(part, token, self.ui.token_grid)
                                
                self.logprint(f"{current_card['name']} with CMC {cmc} was created")
                self.add_item_to_grid(current_card, card_loc, self.ui.history_grid)

                pixmap = self._create_scaled_pixmap(card_loc, DISPLAY_SIZE*1.5)
                self.card_print = card_loc
                self.ui.card_display.setPixmap(pixmap)
                self.ui.card_display.setAlignment(Qt.AlignCenter)
            if not found:
                print("No card found")
            self.debounce = False

    def on_loadtokens_click(self):
        if not self.debounce:
            self.debounce = True
            
            self.setEnabled(False)
            
            self.ui.button_loadtokens.setEnabled(False)
            self.ui.button_loadtokens.setText("Loading...")
            QApplication.processEvents()
            
            while self.ui.token_grid_2.count():
                child = self.ui.token_grid_2.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            QApplication.processEvents()
            
            self._load_tokens_optimized()
    
    def _update_token_status(self, stage, progress=None, details=None):
        """Update token loading status with multi-line format to avoid jarring text changes."""
        global token_progress
        
        try:
            if not self.ui or not hasattr(self.ui, 'button_loadtokens'):
                return
                
            lines = ["Loading All Tokens"]
            
            # Update global token progress
            if progress is not None:
                token_progress = progress
            
            if stage == "displaying":
                lines.append(f"🖼️ Displaying: {progress}% added")
                if details:
                    lines.append(f"📈 Status: {details}")
            elif stage == "complete":
                lines = [f"Load All Tokens ({details} loaded)"]
                token_progress = 100
            elif stage == "error":
                lines = [f"Error: {details}"]
                token_progress = 0
            else:
                lines.append(f"📊 Progress: {token_progress}%")
            
            # Join lines with newlines to create multi-line text
            status_text = "\n".join(lines)
            self.ui.button_loadtokens.setText(status_text)
            QApplication.processEvents()
            
        except RuntimeError:
            pass  # UI object deleted
            self.ui.button_loadtokens.raise_()
            QApplication.processEvents()
            
        except RuntimeError:
            pass  # UI object deleted

    def _load_tokens_optimized(self):
        """Highly optimized token loading with concurrent processing and batched UI updates."""
        try:
            if not self.ui or not hasattr(self.ui, 'button_loadtokens'):
                return
                
            # Pre-filter tokens for better performance
            filtered_tokens = [
                token for token in self.card_data['Token']
                if not any(ignore in token['name'] for ignore in TOKEN_IGNORE_LIST)
            ]
            
            # Sort tokens to put favorites first
            favorites = self.card_data['settings'].get('favorites', [])
            favorite_tokens = []
            regular_tokens = []
            
            for token in filtered_tokens:
                token_id = token.get('oracle_id', token.get('id', ''))
                if token_id in favorites:
                    favorite_tokens.append(token)
                else:
                    regular_tokens.append(token)
            
            # Combine favorites first, then regular tokens
            tokens_to_process = favorite_tokens + regular_tokens
            
            total_tokens = len(tokens_to_process)
            
            self._update_token_status("preparing", details=f"{total_tokens} tokens ({len(favorite_tokens)} favorites)")
            
            if not tokens_to_process:
                self._finish_token_loading(0)
                return
            
            
            def load_single_token(token_data):
                """Load a single token's images and return UI data."""
                token, token_index = token_data
                try:
                    card_locs = self._get_token_images(token)
                    ui_elements = []
                    
                    for cl in card_locs:
                        if os.path.exists(cl):
                            # Pre-load pixmap data
                            pixmap = QPixmap(cl).scaled(
                                QSize(250, 250), 
                                aspectMode=Qt.KeepAspectRatio, 
                                mode=Qt.SmoothTransformation
                            )
                            if not pixmap.isNull():
                                ui_elements.append({
                                    'pixmap': pixmap,
                                    'object_name': cl.split('/')[1].split('.')[0],
                                    'file_path': cl
                                })
                    
                    return token_index, ui_elements, None
                    
                except Exception as e:
                    return token_index, [], str(e)
            
            # Process tokens concurrently
            processed_count = 0
            total_ui_elements = []
            
            # Use smaller batches for better progress updates
            batch_size = 25
            max_workers = min(4, len(tokens_to_process))
            
            for batch_start in range(0, total_tokens, batch_size):
                if not self.isVisible():
                    break
                    
                batch_end = min(batch_start + batch_size, total_tokens)
                batch_tokens = [(tokens_to_process[i], i) for i in range(batch_start, batch_end)]
                
                batch_info = f"{batch_start + 1}-{batch_end} of {total_tokens}"
                self._update_token_status("processing", details=batch_info)
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_token = {
                        executor.submit(load_single_token, token_data): token_data 
                        for token_data in batch_tokens
                    }
                    
                    for future in as_completed(future_to_token):
                        if not self.isVisible():
                            break
                            
                        token_index, ui_elements, error = future.result()
                        processed_count += 1
                        
                        if error:
                            print(f"Error loading token {token_index}: {error}")
                        else:
                            total_ui_elements.extend(ui_elements)
                        
                        if processed_count % 5 == 0 or processed_count == total_tokens:
                            progress = int((processed_count / total_tokens) * 100)
                            details = f"{processed_count}/{total_tokens} tokens"
                            self._update_token_status("loading", progress=progress, details=details)
            
            self._update_token_status("displaying", progress=0, details="Starting display update")
            
            self._batch_add_tokens_to_grid(total_ui_elements)
            self._finish_token_loading(len(total_ui_elements))
            
        except Exception as e:
            print(f"Error in token loading: {e}")
            self._finish_token_loading(0, f"Error: {str(e)}")
    
    def _batch_add_tokens_to_grid(self, ui_elements):
        """Add all token UI elements to the grid in batches for better performance."""
        if not ui_elements or not self.ui or not hasattr(self.ui, 'token_grid_2'):
            return
            
        batch_size = 20
        total_elements = len(ui_elements)
        
        for i in range(0, total_elements, batch_size):
            if not self.isVisible():
                break
                
            batch_end = min(i + batch_size, total_elements)
            
            for j in range(i, batch_end):
                element = ui_elements[j]
                
                try:
                    new_card = QLabel()
                    new_card.setPixmap(element['pixmap'])
                    new_card.objectName = {element['object_name']}
                    new_card.setAlignment(Qt.AlignCenter)
                    
                    # Add visual indicator for favorite tokens
                    token_id = element['object_name']
                    if token_id in self.card_data['settings'].get('favorites', []):
                        new_card.setStyleSheet("border: 3px solid gold; border-radius: 5px;")
                        new_card.setToolTip("⭐ Favorite Token")
                    else:
                        new_card.setStyleSheet("")
                    
                    # Calculate grid position
                    row = j // 8
                    col = j % 8
                    
                    self.ui.token_grid_2.addWidget(new_card, row, col)
                    new_card.mousePressEvent = functools.partial(
                        self.grid_item_click, 
                        source_object=new_card
                    )
                except RuntimeError:
                    break  # UI deleted
            
            progress = int(((batch_end) / total_elements) * 100)
            details = f"{batch_end}/{total_elements} tokens added"
            self._update_token_status("displaying", progress=progress, details=details)
    
    def _finish_token_loading(self, count, error_msg=None):
        """Finish token loading and re-enable the interface."""
        try:
            if not self.ui or not hasattr(self.ui, 'button_loadtokens'):
                return
                
            if error_msg:
                self._update_token_status("error", details=error_msg)
            else:
                self._update_token_status("complete", details=count)
            
            self.ui.button_loadtokens.setEnabled(True)
            
            self.setEnabled(True)
            self.debounce = False
            
        except RuntimeError:
            self.debounce = False
    
    def _get_token_images(self, token):
        """Get image paths for a token, downloading if necessary and online."""
        card_locs = []
        
        oracle_id = token.get('oracle_id', token.get('id', ''))
        if not oracle_id:
            return card_locs
        
        base_path = f'Images/{oracle_id}.png'
        
        if os.path.exists(base_path):
            card_locs.append(base_path)
            
            face_count = 1
            while True:
                face_path = f'Images/{oracle_id}-{face_count}.png'
                if os.path.exists(face_path):
                    card_locs.append(face_path)
                    face_count += 1
                else:
                    break
                    
        elif self.card_data['settings']['Online']:
            try:
                if token.get('image_uris', {}).get('border_crop'):
                    downloaded_path = download_img(token['image_uris']['border_crop'], oracle_id)
                    if downloaded_path and os.path.exists(downloaded_path):
                        card_locs.append(downloaded_path)
                
                elif token.get('card_faces'):
                    for face_count, face in enumerate(token['card_faces']):
                        if face.get('image_uris', {}).get('border_crop'):
                            suffix = f"-{face_count}" if face_count > 0 else ""
                            downloaded_path = download_img(
                                face['image_uris']['border_crop'], 
                                f'{oracle_id}{suffix}'
                            )
                            if downloaded_path and os.path.exists(downloaded_path):
                                card_locs.append(downloaded_path)
                                
            except Exception as e:
                if "timeout" not in str(e).lower():
                    print(f"Error downloading token {token.get('name', 'unknown')}: {e}")
        
        return card_locs

    def on_check(self, state):
        if not self.debounce:
            self.debounce = True
            self.setEnabled(False)
            setting = self.sender().objectName().split('_')[1].capitalize()
            if setting in self.card_data['settings']['type_toggles'].keys():
                self.card_data['settings']['type_toggles'][setting] = True if state else False
                self.setup_cur_data()
            else:
                self.card_data['settings'][setting] = True if state else False
            with open('json/settings.json', 'w') as json_file:
                json.dump(self.card_data['settings'], json_file, indent=4)
            
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
        pixmap_card = self._create_scaled_pixmap(img_loc, QSize(300, 300))
        new_card.setPixmap(pixmap_card)
        new_card.setAlignment(Qt.AlignCenter)
        grid.addWidget(new_card, 0, 0)
        new_card.mousePressEvent = functools.partial(self.grid_item_click, source_object=new_card, grid=grid.objectName().split('_')[0])

    def grid_item_click(self, event, source_object:QLabel = None, grid = 'token'):
        image_path = f'Images/{str(source_object.objectName).strip('{\'}')}.png'
        pixmap = self._create_scaled_pixmap(image_path, DISPLAY_SIZE)
        
        # Extract token ID from the source object name
        token_id = str(source_object.objectName).strip('{\'}')
        
        if grid == 'token':
            self.ui.token_display.setPixmap(pixmap)
            self.ui.token_display_2.setPixmap(pixmap)
            self.ui.token_display.setAlignment(Qt.AlignCenter)
            self.ui.token_display_2.setAlignment(Qt.AlignCenter)
            self.token_print = image_path
            
            # Update selected token for favoriting
            self.selected_token_id = token_id
            self._update_favorite_button_text()
            
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
    if getattr(sys, 'frozen', False):
        font_id = QFontDatabase.addApplicationFont(f"{APP_PATH}\\Planewalker-38m6.ttf")
    else:
        font_id = QFontDatabase.addApplicationFont(f"{APP_PATH}\\Data\\Planewalker-38m6.ttf")
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            print("Font loaded")
            font = QFont(font_families[0])
            app.setFont(font)
        else:
            print("Font not loaded")
    else:
        pass
    window = LoadingWindow()
    window.show()
    sys.exit(app.exec())