import win32print
import win32ui
from PIL import Image, ImageWin

def print_card(file_name):
    printer_name = win32print.GetDefaultPrinter ()

    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)

    bmp = Image.open(file_name)
    if bmp.size[0] > bmp.size[1]:
        bmp = bmp.rotate (90)

    hDC.StartDoc (file_name)
    hDC.StartPage ()

    dib = ImageWin.Dib (bmp)

    dib.draw(hDC.GetHandleOutput(),(0,0,bmp.size[0],bmp.size[1]))

    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()