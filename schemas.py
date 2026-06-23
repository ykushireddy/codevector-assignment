from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class CursorResponse(BaseModel):
    updated_at: datetime
    id: int


class ProductsListResponse(BaseModel):
    products: list[ProductResponse]
    next_cursor: CursorResponse | None