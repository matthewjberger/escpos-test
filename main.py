# Dependencies:
# pip3 install python-escpos

from multiprocessing import dummy
from escpos.printer import Network, Dummy
import base64
import os

def print_chit(ip_address, base64_image):
    path = "output.png"
    try:
        with open(path, "wb") as fh:
            fh.write(base64.decodebytes(base64_image))
        printer = Network(ip_address)
        printer.image(path)
        printer.cut()
    finally:
        if os.path.exists(path):
            os.remove(path)


def print_image(printer_ip_address, path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        print_chit(printer_ip_address, encoded_string)


print_image("127.0.0.1", "chit.png")
