from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
db_path = (BASE_DIR / "english_app.db").resolve()
DB_URL = f"sqlite+aiosqlite:///{db_path.as_posix()}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )
    PORT: int = '8000'
    RELOAD: bool = 'False'
    HOST: str = '127.0.0.1'
    EMAIL: str = 'example@example.com'
    API_URL: str = "https://api.mymemory.translated.net/"
    API_GEMINI: str | None = None
    USE_GEMINI: bool = False

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )
    URL: str = DB_URL


settings = Settings() # type: ignore
db_settings = DatabaseSettings()

BASE_URL = f"{settings.HOST}:{settings.PORT}"


