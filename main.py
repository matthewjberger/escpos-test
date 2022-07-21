from escpos import *
from PIL import Image
from io import BytesIO
import base64
import threading


class Printer:
    _lock = threading.Lock()

    def __init__(self, ip_address, port=9100) -> None:
        self.printer = printer.Network(ip_address, port)

    def paper_status(self):
        self.printer.paper_status()

    def is_online(self):
        self.printer.is_online()

    def print_file(self, path, thread_id):
        with self._lock:
            with open(path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read())
                image = Image.open(BytesIO(base64.b64decode(base64_image)))
                print(f"[Thread {thread_id}] Printing chit...")
                self.printer.image(image)
                self.printer.cut()
                print(f"[Thread {thread_id}] Printing succeeded.")


printer = Printer("192.168.0.172")


class print_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        printer.print_file("chit.png", self.threadID)


threads = list()
for index in range(3):
    thread = print_thread("Thread " + str(index), index, )
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
