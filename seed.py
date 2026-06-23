import os
import random
from datetime import datetime
from decimal import Decimal

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import Product

load_dotenv()

fake = Faker()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

TOTAL_PRODUCTS = 200_000
BATCH_SIZE = 10_000

CATEGORIES = [
    "Electronics",
    "Books",
    "Clothing",
    "Home",
    "Sports",
    "Beauty"
]


def generate_batch(size):
    rows = []

    for _ in range(size):
        rows.append(
            {
                "name": fake.catch_phrase(),
                "category": random.choice(CATEGORIES),
                "price": Decimal(
                    str(
                        round(
                            random.uniform(10, 5000),
                            2
                        )
                    )
                ),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )

    return rows


def main():

    inserted = 0

    with Session(engine) as session:

        while inserted < TOTAL_PRODUCTS:

            batch = generate_batch(BATCH_SIZE)

            session.bulk_insert_mappings(
                Product,
                batch
            )

            session.commit()

            inserted += len(batch)

            print(
                f"Inserted {inserted}/{TOTAL_PRODUCTS}"
            )


if __name__ == "__main__":
    main()