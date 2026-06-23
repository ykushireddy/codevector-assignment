from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.sql import func

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    category = Column(String(100), nullable=False)

    price = Column(Numeric(10, 2), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        Index(
            "idx_products_updated_id",
            "updated_at",
            "id",
            postgresql_using="btree"
        ),

        Index(
            "idx_products_category_updated_id",
            "category",
            "updated_at",
            "id",
            postgresql_using="btree"
        ),
    )
