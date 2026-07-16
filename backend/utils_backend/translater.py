import logging
import asyncio

from backend.config import settings
from aiohttp import ClientSession
from fastapi import HTTPException
from google import genai
import translators as ts


async def translate_with_genai(text_to_translate: str, from_lang, to_lang, proxy):
    client = genai.Client(
        api_key=settings.API_GEMINI,
        http_options=proxy
    )
    prompt = f"Переведи этот текст c {from_lang} языка на {to_lang} язык. Сохраняй естественный стиль. Выведи ТОЛЬКО перевод: {text_to_translate}"
    response = await client.aio.models.generate_content(
        model='gemini-3.5-flash', 
        contents=prompt,
    )
    if response.text:
        return response.text

async def translate_with_mymemoryapi(text: str, from_lang, to_lang):
    url = settings.API_URL
    params = {
        "q": text,
        "langpair": f"{from_lang}|{to_lang}",
        "de": settings.EMAIL
    }
    async with ClientSession() as session:
        response = await session.get(url, params=params, timeout = 10)
        if response.status !=  200:
            raise HTTPException(status_code=400, detail='MyMemory API ERROR')
        data = await response.json()
        if data.get('responseStatus') != 200: 
            error_msg = data.get("responseDetails", "Unknown error")
            raise HTTPException(status_code=400, detail=f"MyMemory Error: {error_msg}")
        translated_word =  data["responseData"]["translatedText"]   
        if translated_word.lower() == text.lower():
            raise HTTPException(status_code=400, detail=f"Can't translate automaticly")
        return translated_word

async def translate(text: str, from_lang='en', to_lang='ru'):
    try:
        translated = await ts.translate_text(
                text, 
                translator='google', 
                from_language='en', 
                to_language='ru', 
                http_client='aiohttp', 
                if_use_async=True
            )
        if translated:
            return str(translated).capitalize()
    except Exception as e:
        logging.warning(f"Ошибка translators: {e}. Переходим к MyMemory...")
    try:
        result = await translate_with_mymemoryapi(text, from_lang, to_lang)
        if result:
            return result.capitalize()
    except Exception as e:
        logging.warning(f"Ошибка MyMemory: {e}. Переходим к Gemini...")
    if settings.USE_GEMINI:    
        try:
            proxy = genai.types.HttpOptions(
                client_args={'proxy': 'socks5://127.0.0.1:10808'},
                async_client_args={'proxy': 'socks5://127.0.0.1:10808'}
            )
            result = await translate_with_genai(text, from_lang, to_lang, proxy)
            if result:
                return result.capitalize()
        except Exception as e:
            logging.error(f"Ошибка Gemini: {e}")
