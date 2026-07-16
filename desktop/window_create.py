import webview
from config import BASE_DIR
from desktop.api import api

def create_window():
    window = webview.create_window(
        js_api=api,
        title='LookmaxEng',
        url='http://127.0.0.1:8000',
        width=1000,
        height=700,
        resizable=True,
    )
    webview.start(icon=str(BASE_DIR/'favicon.ico'))

    