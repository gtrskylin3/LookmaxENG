import webbrowser
from backend.config import settings
from finder import start_hotkeys
from server import start_server
from threading import Thread
from utils.enable_dpi_awareness import enable_dpi_awareness

if __name__ == '__main__':
    enable_dpi_awareness()
    webbrowser.open_new_tab('http://127.0.0.1:8000')
    hotkey_thread = Thread(target=start_hotkeys, daemon=True)
    hotkey_thread.start()
    start_server()
   
    