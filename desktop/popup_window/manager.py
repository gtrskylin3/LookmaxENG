import time 
import webview
import threading
from jinja2 import Environment, FileSystemLoader

# Настраиваем загрузчик шаблонов из папки "templates"
env = Environment(loader=FileSystemLoader('backend/templates'))

class PopupManager:
    def __init__(self):
        self.window = None
        self.close_timer = None

    def set_window(self, window):
        """Передаем сюда объект окна, созданный через webview.create_window"""
        self.window = window
    
    def show_popup(self, text: str, translation: str, height: float):
        if not self.window:
            print("Ошибка: Окно popup не привязано к PopupManager!")
            return
        
        if self.close_timer:
            self.close_timer.cancel()
        width = 250
        popup_height = 80
        template = env.get_template('popup.html')
        html_content = template.render(
            word=text, 
            translation=translation, 
        )

        self.window.load_html(html_content)
        self.window.resize(width, popup_height)
        self.window.show()

        # Запускаем таймер скрытия
        self.close_timer = threading.Timer(3.0, self.hide_popup)
        self.close_timer.start()
    
    def hide_popup(self):
        if self.window:
            try:
                self.window.hide()
            except Exception:
                pass

popup = PopupManager()