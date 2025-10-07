"""
API Handler for Scryfall Magic: The Gathering API interactions.

This module handles all communication with the Scryfall API including
downloading card data, images, and managing bulk data updates.
"""

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
import time
import threading

import requests

# API Configuration
API_URL = 'https://api.scryfall.com/'

# Concurrent download configuration
MAX_CONCURRENT_DOWNLOADS = 10  # Conservative limit to be API-friendly
DOWNLOAD_TIMEOUT = 30  # Timeout for individual downloads
RETRY_ATTEMPTS = 3  # Number of retry attempts for failed downloads

# Search strings for different card types
CREATURE_STR = '+type%3Acreature'
BLOCK_UN_STR = '+not%3Afunny+-set%3Aunf'

# Thread-safe session for downloads
_session_lock = threading.Lock()
_session = None

def get_session() -> requests.Session:
    """Get or create a thread-safe requests session."""
    global _session
    if _session is None:
        with _session_lock:
            if _session is None:
                _session = requests.Session()
                _session.headers.update({
                    'User-Agent': 'Momir/1.0 (Bulk Image Downloader)'
                })
    return _session

# Token search configurations
TOKEN_SEARCHES = [
    'cards/search?q=layout:token&order=name',
    'cards/search?q=layout:emblem&order=name', 
    'cards/search?q=type:Dungeon&order=name',
    'cards/search?q=layout:double_faced_token+-type:Token+-name:Bounty+-set_type:minigame+-type:Dungeon&order=name'
]
TOKEN_TYPES = ['Token', 'Card', 'Dungeon', 'Emblem']
TOKEN_IGNORE_LIST = [' Ad', 'Decklist', ' Bio', 'Checklist', 'Punchcard']


def get_card(card_name: str) -> Dict[str, Any]:
    """
    Retrieve a single card by name from the Scryfall API.
    
    Args:
        card_name: Name of the card to search for
        
    Returns:
        Dictionary containing card data
        
    Raises:
        requests.RequestException: If the API request fails
    """
    response = requests.get(f"{API_URL}cards/named?fuzzy={card_name}")
    response.raise_for_status()
    return response.json()


def get_bulk() -> Dict[str, Any]:
    """
    Retrieve bulk data information from the Scryfall API.
    
    Returns:
        Dictionary containing bulk data information
        
    Raises:
        requests.RequestException: If the API request fails
    """
    response = requests.get(f"{API_URL}bulk-data")
    response.raise_for_status()
    return response.json()


def save_json_file(data: Any, file_path: str) -> None:
    """
    Save data to a JSON file with proper formatting.
    
    Args:
        data: Data to save
        file_path: Path where to save the file
    """
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the loaded data, or None if file doesn't exist
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as json_file:
            return json.load(json_file)
    return None


def download_json_file(url: str, file_path: str) -> Dict[str, Any]:
    """
    Download a JSON file from a URL and save it locally.
    
    Args:
        url: URL to download from
        file_path: Local path to save the file
        
    Returns:
        Dictionary containing the downloaded JSON data
        
    Raises:
        requests.RequestException: If the download fails
    """
    response = requests.get(url)
    response.raise_for_status()
    
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    return response.json()


def download_img(url: str, card_id: Optional[str] = None) -> str:
    """
    Download an image from a URL.
    
    Args:
        url: URL of the image to download
        card_id: Optional ID to use for the filename
        
    Returns:
        File path if card_id provided, otherwise raw content
        
    Raises:
        requests.RequestException: If the download fails
    """
    response = requests.get(url)
    response.raise_for_status()
    
    if card_id:
        file_path = f"Images/{card_id}.png"
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    
    return response.content


def check_bulk_data() -> bool:
    """
    Check if new bulk data is available from Scryfall.
    
    Returns:
        True if new data is available, False otherwise
    """
    try:
        bulk_data = load_json_file('json/bulk.json')
        new_bulk_data = get_bulk()
        
        if bulk_data != new_bulk_data:
            print('New bulk data available')
            save_json_file(new_bulk_data, 'json/bulk.json')
            return True
        
        return False
    except requests.RequestException as e:
        print(f"Error checking bulk data: {e}")
        return False


def find_newest_version(card_id: str, card_list: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Find the newest version of a card from a list of cards.
    
    Args:
        card_id: Oracle ID of the card to find
        card_list: List of card dictionaries to search through
        
    Returns:
        Dictionary of the newest card version, or None if not found
    """
    newest_card = None
    
    for card in card_list:
        if card['oracle_id'] == card_id:
            if not newest_card:
                newest_card = card
            elif datetime.strptime(card['released_at'], '%Y-%m-%d') > \
                 datetime.strptime(newest_card['released_at'], '%Y-%m-%d'):
                newest_card = card
    
    return newest_card


def download_single_image(url: str, file_path: str, max_retries: int = RETRY_ATTEMPTS) -> tuple[bool, str, str]:
    """
    Download a single image with retry logic.
    
    Args:
        url: URL of the image to download
        file_path: Local file path to save the image
        max_retries: Maximum number of retry attempts
        
    Returns:
        Tuple of (success, file_path, error_message)
    """
    session = get_session()
    
    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=DOWNLOAD_TIMEOUT)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            return True, file_path, ""
            
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                return False, file_path, str(e)
            time.sleep(0.1 * (attempt + 1))  # Brief exponential backoff
    
    return False, file_path, "Max retries exceeded"


def download_images_concurrent(
    download_tasks: List[tuple[str, str]], 
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
    max_workers: int = MAX_CONCURRENT_DOWNLOADS
) -> tuple[List[str], List[tuple[str, str]]]:
    """
    Download multiple images concurrently.
    
    Args:
        download_tasks: List of (url, file_path) tuples
        progress_callback: Optional callback function (completed, total, current_file)
        max_workers: Maximum number of concurrent downloads
        
    Returns:
        Tuple of (successful_downloads, failed_downloads)
    """
    if not download_tasks:
        return [], []
        
    successful_downloads = []
    failed_downloads = []
    completed = 0
    total = len(download_tasks)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {
            executor.submit(download_single_image, url, file_path): (url, file_path)
            for url, file_path in download_tasks
        }
        
        for future in as_completed(future_to_task):
            url, file_path = future_to_task[future]
            completed += 1
            
            try:
                success, result_path, error = future.result()
                if success:
                    successful_downloads.append(result_path)
                else:
                    failed_downloads.append((file_path, error))
                    print(f"Failed to download {url}: {error}")
                    
            except Exception as e:
                failed_downloads.append((file_path, str(e)))
                print(f"Exception downloading {url}: {e}")
            
            if progress_callback:
                current_file = os.path.basename(file_path)
                progress_callback(completed, total, current_file)
    
    return successful_downloads, failed_downloads


def download_double_faced_card_concurrent(
    front_url: str, 
    back_url: str, 
    oracle_id: str,
    progress_callback: Optional[Callable[[int, int, str], None]] = None
) -> Optional[str]:
    """
    Download and combine a double-faced card concurrently.
    
    Args:
        front_url: URL of the front face
        back_url: URL of the back face  
        oracle_id: Oracle ID for the final filename
        progress_callback: Optional progress callback
        
    Returns:
        Path to the combined image file, or None if failed
    """
    from .image_handler import flip_card_image
    
    front_temp = f"Images/temp_{oracle_id}_front.png"
    back_temp = f"Images/temp_{oracle_id}_back.png"
    final_path = f"Images/{oracle_id}.png"
    
    if os.path.exists(final_path):
        return final_path
    
    try:
        download_tasks = [
            (front_url, front_temp),
            (back_url, back_temp)
        ]
        
        successful, failed = download_images_concurrent(
            download_tasks, 
            progress_callback=progress_callback,
            max_workers=2
        )
        
        if len(successful) == 2 and os.path.exists(front_temp) and os.path.exists(back_temp):
            with open(front_temp, 'rb') as f:
                front_bytes = f.read()
            with open(back_temp, 'rb') as f:
                back_bytes = f.read()
            
            combined_path = flip_card_image(front_bytes, back_bytes, oracle_id)
            
            for temp_file in [front_temp, back_temp]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
            return combined_path
            
        else:
            print(f"Failed to download both faces for {oracle_id}. Successful: {len(successful)}, Failed: {len(failed)}")
            return None
            
    except Exception as e:
        print(f"Error processing double-faced card {oracle_id}: {e}")
        return None
    finally:
        for temp_file in [front_temp, back_temp]:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass