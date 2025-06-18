from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from app.core.database import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    # add ext fields
    pass
