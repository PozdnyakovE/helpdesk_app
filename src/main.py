from fastapi import FastAPI
import uvicorn

from app.api.routers import main_router
from app.core.config import settings


app = FastAPI(title=settings.APP_TITLE,
              description=settings.APP_DESCRIPTION,
              )


app.include_router(main_router)


def main() -> None:
    """Функция запуска приложения."""
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT)


if __name__ == '__main__':
    main()
