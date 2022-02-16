from escpos import *
from PIL import Image
from io import BytesIO
import base64
import os

def print_chit(ip_address, base64_image):
    pilImg = Image.open(BytesIO(base64.b64decode(base64_image)))

    lpt = printer.Network(ip_address)
    print(lpt.paper_status())
    print(lpt.is_online())
        
    lpt.image(pilImg)
    lpt.cut()

def print_image(printer_ip_address, path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        print_chit(printer_ip_address, encoded_string)

print_image("192.168.1.40", "chit.png")
