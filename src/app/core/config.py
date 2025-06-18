import os

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Статические настройки приложения."""

    APP_TITLE: str = 'Helpdesk-система'
    APP_DESCRIPTION: str = (
        'Информационная система службы поддержки')
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000
    RELOAD: bool = False
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    # MAX_LENGTH_EMAIL: int = 512
    # MAX_LENGTH_USERNAME: int = 512
    # MAX_LENGTH_PASSWORD: int = 256
    # MAX_LENGTH_FORMAT_MSG: int = 20
    # MAX_LENGTH_NAME_CHANNEL: int = 100
    # MAX_LENGTH_NAME_TEMPLATE: int = 256
    # MAX_LENGTH_STATUS_MSG: int = 10
    # DEFAULT_ADMIN_NAME: str
    # DEFAULT_ADMIN_PASSWORD: str
    # DEFAULT_USER_ROLE: str = 'user'
    # DEFAULT_ADMIN_ROLE: str = 'admin'
    # SEND_SETTING_ATTEMPTS: int = 3
    # SEND_SETTING_TIMEOUT: int = 30
    # MINUTES_EXPIRED_FOR_JWT: int = 30
    # DAYS_EXPIRED_FOR_REFRESH_JWT: int = 30
    # SECRET_KEY: str
    # ALGORITHM: str
    # MAX_LENGTH_SUBJECT_MSG: int = 256
    # TEMPLATE_DEFAULT_PARAMETER: str = 'не задано'
    # SMTP_HOST: str
    # SMTP_PORT: int
    # SMTP_ADDRESS: str
    # SMTP_PASSWORD: str
    # SUPPRESSED_LOGGERS: list[str] = ['uvicorn', 'uvicorn.error',
    #                                  'fastapi', 'uvicorn.access']
    # LOG_DIR: str = 'logs'
    # LOG_FORMAT: str = (
    #     '{time:HH:mm:ss} | {level} | {extra[endpoint]} | {message}')
    # LOG_DATE_FORMAT: str = '%Y-%m-%d'
    # LOG_FILE_ENCODING: str = 'utf-8'
    # LOG_ROTATION: str = '00:00'
    # LOG_RETENTION: str = '7 days'
    # LOG_COMPRESSION: str = 'zip'
    # LOG_LEVEL: str = 'DEBUG'

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '../../../infra', '.env'),
        env_file_encoding='utf-8',
        extra='ignore')

    def get_db_url(self) -> str:
        """Ссылка для подключения к базе данных."""
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}')


try:
    settings = Settings()
except ValidationError as error:
    raise EnvironmentError(
        f'Отсутствует переменная окружения: {error.errors()[0]["loc"][0]}')
