from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .database import get_db
from .models import Product
from .schemas import ProductsListResponse

router = APIRouter()


@router.get(
    "/products",
    response_model=ProductsListResponse
)
def get_products(
    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    category: str | None = None,
    cursor_updated_at: datetime | None = None,
    cursor_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(
            Product.category == category
        )

    if cursor_updated_at and cursor_id:

        query = query.filter(
            or_(
                Product.updated_at < cursor_updated_at,

                and_(
                    Product.updated_at == cursor_updated_at,
                    Product.id < cursor_id
                )
            )
        )

    products = (
        query
        .order_by(
            desc(Product.updated_at),
            desc(Product.id)
        )
        .limit(limit + 1)
        .all()
    )

    has_next = len(products) > limit

    products = products[:limit]

    next_cursor = None

    if has_next and products:
        last = products[-1]

        next_cursor = {
            "updated_at": last.updated_at,
            "id": last.id
        }

    return {
        "products": products,
        "next_cursor": next_cursor
    }