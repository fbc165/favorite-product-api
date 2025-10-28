# Os models da API devem ser todos importados aqui
from favorite_product_api.users.models import User

from .base import Base
from .session import engine, get_db

__all__ = [
    "Base",
    "engine",
    "get_db",
    "User",
]
