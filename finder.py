import asyncio
from threading import Thread
from fastapi.responses import RedirectResponse
import requests
from utils.ocr import parse_image
from config import BASE_DIR, IMAGE_DIR
from pynput.mouse import Controller as MouseController
from pynput import keyboard
from PIL import ImageGrab
from config import WIDTH, HEIGHT
from schemes.word import Word
from aiohttp import ClientSession
from backend.config import BASE_URL
from desktop.popup_window.manager import popup

mouse = MouseController()

def capture_region(x: int, y: int):
    left = x - WIDTH // 2
    top = y - HEIGHT // 2
    right = left + WIDTH
    bottom = top + HEIGHT
    bbox = bbox=(left, top, right, bottom)
    screenshot = ImageGrab.grab(bbox)
    return screenshot, left, top
    
def recognize(screenshot, language: str = 'en'):
    image_text, image_words = parse_image(screenshot, language)
    return image_text, image_words

def find_word(words: list[Word], mouse_x, mouse_y):
    for word in words:
        if word.contains(mouse_x, mouse_y):
            return word
    
def ocr_main():
    x, y = mouse.position
    screenshot, left, top = capture_region(x, y)
    image_text, words = recognize(screenshot, 'en')
    mouse_x = x - left
    mouse_y = y - top
    word = find_word(words, mouse_x, mouse_y)
    if word:
        json = {
                "word": word.text,
                "translate": None,
                "context": None
            }
        response = requests.post(f"http://{BASE_URL}/api/words", json=json)
        data = response.json()
        text = data.get('word')
        global_word_x = left + word.x
        global_word_y = top + word.y

        translate = data.get('translate')
        popup.show_popup(text, translate, word.height)
        

def start_hotkeys():
    keys = ['q', 'й']
    
    # Автоматически собираем словарь хоткеев
    hotkeys_map = {
        f'<shift>+<alt>+{k}': lambda: Thread(target=ocr_main, daemon=True).start()
        for k in keys
    }
    with keyboard.GlobalHotKeys(hotkeys_map) as listener:
        listener.join()
