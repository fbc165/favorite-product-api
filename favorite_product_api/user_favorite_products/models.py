from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from favorite_product_api.databases.postgresql.base import Base


class UserFavoriteProduct(Base):
    __tablename__ = "user_favorite_product"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_id = Column(Integer, nullable=False, index=True, unique=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship(
        "User",
        back_populates="favorite_products",
    )
