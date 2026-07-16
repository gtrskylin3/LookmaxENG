import time
import webbrowser

import webview
from backend.config import settings
from config import BASE_DIR
from desktop.window_create import create_window
from finder import start_hotkeys
from server import start_server
from threading import Thread
from utils.enable_dpi_awareness import enable_dpi_awareness

if __name__ == '__main__':
    enable_dpi_awareness()
    hotkey_thread = Thread(target=start_hotkeys, daemon=True)
    hotkey_thread.start()
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    create_window()
    time.sleep(1)
   
        

    