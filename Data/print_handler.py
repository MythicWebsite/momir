"""
Print Handler for printing Magic: The Gathering card images.

This module handles printing card images to the default printer with
proper formatting and orientation.
"""

import win32print
import win32ui
from PIL import ImageWin

from Data.image_handler import convert_card


def print_card(file_path: str) -> None:
    """
    Print a card image to the default printer.
    
    Args:
        file_path: Path to the image file to print
        
    Raises:
        Exception: If printing fails or no default printer is available
    """
    if not file_path:
        print("No image file provided for printing")
        return
        
    try:
        printer_name = win32print.GetDefaultPrinter()
        
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)

        processed_image = convert_card(file_path, img_return=True)
        
        if processed_image.size[0] > processed_image.size[1]:
            processed_image = processed_image.rotate(90, expand=True)

        hDC.StartDoc(f"Magic Card - {file_path}")
        hDC.StartPage()

        dib = ImageWin.Dib(processed_image)

        dib.draw(
            hDC.GetHandleOutput(),
            (0, 0, processed_image.size[0], processed_image.size[1])
        )

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
        
        print(f"Successfully printed card: {file_path}")
        
    except Exception as e:
        print(f"Error printing card {file_path}: {e}")
        raise