import asyncio
from pathlib import Path
from winrt.windows.media.ocr import OcrEngine, OcrResult
from winrt.windows.globalization import Language
from winrt.windows.storage.streams import DataWriter
from winrt.windows.graphics.imaging import SoftwareBitmap, BitmapPixelFormat
from PIL import Image

from schemes.word import Word

def recognize_bytes(bytes, width, height, lang='en'):
    cmd = 'Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0"'
    assert OcrEngine.is_language_supported(Language(lang)), cmd
    writer = DataWriter()
    writer.write_bytes(bytes)
    sb = SoftwareBitmap.create_copy_from_buffer(writer.detach_buffer(), BitmapPixelFormat.RGBA8, width, height)
    return OcrEngine.try_create_from_language(Language(lang)).recognize_async(sb)

def recognize_pil(img, lang='en'):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return recognize_bytes(img.tobytes(), img.width, img.height, lang)


def recognize_pil_sync(img, lang='en') -> OcrResult:
    return asyncio.run(recognize_pil(img, lang))

def parse_words(data: OcrResult):
    return [
        Word(
            text=''.join(i for i in w.text if i.isalpha()),
            x=w.bounding_rect.x,
            y=w.bounding_rect.y,
            width=w.bounding_rect.width,
            height=w.bounding_rect.height,
        ) 
        for l in data.lines
        for w in l.words
    ]

def parse_image(image: Image, language: str):
    result = recognize_pil_sync(image, language)
    return result.text, parse_words(result)


