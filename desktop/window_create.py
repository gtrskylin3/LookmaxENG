import os

import webview
from config import BASE_DIR
from desktop.api import api
from desktop.popup_window.manager import popup

def on_closed():
    print("Окно закрыто. Принудительно завершаем все фоновые процессы...")
    os._exit(0)

def create_window():
    window = webview.create_window(
        js_api=api,
        title='LookmaxEng',
        url='http://127.0.0.1:8000',
        width=1000,
        height=700,
        resizable=True,
    )
    window.events.closed += on_closed
    popup_win = webview.create_window(
        title="Translation Popup",
        width=250,
        height=80,
        frameless=True,
        on_top=True,
        easy_drag=False,
        hidden=True  # Оно не появится на экране при старте
    )
    
    # Связываем созданное окно с менеджером
    popup.set_window(popup_win)
    # 4. Запускаем графический движок (блокирует главный поток до закрытия главного окна)
    webview.start(icon=str(BASE_DIR/'favicon.ico'))