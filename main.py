from ocr import parse_image
from config import BASE_DIR, IMAGE_DIR
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from PIL import ImageGrab
from config import WIDTH, HEIGHT
import ctypes

from schemes.word import Word

# --- ВАЖНО: Включаем DPI Awareness для Windows перед любыми действиями ---
try:
    # Вариант для Windows 8.1 и 10/11 (Per Monitor DPI Aware)
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # 1.3.5
except AttributeError:
    try:
        # Старый вариант для Windows 7/8
        ctypes.windll.user32.SetProcessDPIAware() # 1.2.1
    except AttributeError:
        pass  # Если запуск не на Windows

mouse = MouseController()
keyboard = KeyboardController()

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
    
    

def main():
    x, y = mouse.position
    screenshot, left, top = capture_region(x, y)
    image_text, words = recognize(screenshot, 'en')
    mouse_x = x - left
    mouse_y = y - top
    word = find_word(words, mouse_x, mouse_y)
    if word:
        print(word.text)

if __name__ == '__main__':
    from pynput import keyboard
    hotkeys_map = {
        '<shift>+<alt>+q': main
    }
    with keyboard.GlobalHotKeys(hotkeys_map) as listener:
        listener.join()
