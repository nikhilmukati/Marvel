from threading import Thread
from src.main.SearchDirectory.lookupDriveChange import lookup
from ctypes import windll
import string


def get_drives():
    drives = []
    bit_mask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bit_mask & 1:
            drives.append(letter)
        bit_mask >>= 1

    return drives


def read_dir():
    drives = get_drives()
    for drive in drives:
        t = Thread(target=lookup(drive+':\\'))
        t.daemon = True
        t.start()

