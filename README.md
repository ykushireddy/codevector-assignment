# Product Catalog API

A FastAPI + PostgreSQL backend built for the CodeVector Backend Take-Home Assignment.

## Overview

This project provides an API for browsing approximately 200,000 products with:

* Fast pagination
* Category filtering
* Cursor-based pagination
* PostgreSQL database
* SQLAlchemy ORM
* FastAPI REST API

The system is designed to handle large datasets efficiently while ensuring users do not see duplicate products or miss products when new records are inserted or updated during browsing.

---

## Tech Stack

* FastAPI
* PostgreSQL (Neon)
* SQLAlchemy ORM
* Python 3.13
* Faker
* Uvicorn

---

## Database Schema

### Product

| Field      | Type                  |
| ---------- | --------------------- |
| id         | Integer (Primary Key) |
| name       | String                |
| category   | String                |
| price      | Numeric(10,2)         |
| created_at | Timestamp             |
| updated_at | Timestamp             |

---

## API Endpoint

### GET /products

Returns products ordered by newest first.

### Query Parameters

| Parameter         | Description                                        |
| ----------------- | -------------------------------------------------- |
| limit             | Number of records per page (default: 20, max: 100) |
| category          | Optional category filter                           |
| cursor_updated_at | Cursor timestamp from previous page                |
| cursor_id         | Cursor id from previous page                       |

### Example

GET /products?limit=20

GET /products?category=Books&limit=20

GET /products?limit=20&cursor_updated_at=2026-06-23T14:09:45.871927Z&cursor_id=199981

---

## Cursor Pagination

Products are sorted using:

```sql
ORDER BY updated_at DESC, id DESC
```

The next page uses:

```sql
WHERE
(
    updated_at < :cursor_updated_at
)
OR
(
    updated_at = :cursor_updated_at
    AND id < :cursor_id
)
```

### Why Cursor Pagination?

OFFSET pagination becomes slower as page numbers increase because the database must scan and skip rows.

Cursor pagination:

* Scales efficiently for large datasets
* Provides stable ordering
* Avoids duplicate records
* Prevents missing records when new data is inserted

---

## Performance Optimizations

### Indexes

```sql
CREATE INDEX idx_products_updated_id
ON products(updated_at DESC, id DESC);
```

Optimizes product listing and cursor pagination.

```sql
CREATE INDEX idx_products_category_updated_id
ON products(category, updated_at DESC, id DESC);
```

Optimizes category-filtered pagination queries.

---

## Seed Script

The project includes a seed script that generates 200,000 products.

### Features

* Uses Faker to generate realistic product names
* Uses batch inserts
* Inserts records in chunks of 10,000
* Uses SQLAlchemy bulk_insert_mappings for improved performance

### Run

```bash
python -m scripts.seed
```

---

## Local Setup

### Clone Repository

```bash
git clone <repository-url>
cd codevector-task
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
```

### Run Application

```bash
uvicorn app.main:app --reload
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Deployment

### Backend

Hosted on Render.

### Database

Hosted on Neon PostgreSQL.

### Environment Variable

```env
DATABASE_URL=<neon_connection_string>
```

---

## Project Structure

```text
project/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes.py
│
├── scripts/
│   └── seed.py
│
├── requirements.txt
├── .env.example
├── render.yaml
└── README.md
```

---

## Improvements With More Time

* Add Alembic migrations
* Add automated tests
* Add Docker support
* Add caching using Redis
* Add monitoring and logging
* Add API rate limiting

---

## AI Usage

AI tools (ChatGPT) were used to:

* Generate initial project structure
* Discuss pagination approaches
* Review implementation choices
* Explain FastAPI and SQLAlchemy patterns

All generated code was reviewed, tested, debugged, and modified during implementation.

---

## Assignment Requirements Covered

* FastAPI backend
* PostgreSQL database
* SQLAlchemy ORM
* 200,000 generated products
* Category filtering
* Cursor pagination
* Newest-first ordering
* Performance indexes
* next_cursor support
* Bulk data generation
* Deployable to Render
* Hosted database on Neon
