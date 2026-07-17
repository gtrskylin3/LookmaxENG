from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "media"
WIDTH: int = 640
HEIGHT: int = 480

class Settings(BaseSettings):
    SettingsConfigDict(env_file=BASE_DIR / '.env')

settings = Settings()

