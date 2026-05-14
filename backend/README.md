# RAG Healthcare Assistant — Backend

A FastAPI-based backend for a Healthcare RAG (Retrieval-Augmented Generation) Assistant with:

- JWT Authentication
- Role-Based Access Control (RBAC)
- PDF Ingestion
- Hybrid Search (Semantic + BM25)
- PostgreSQL + PGVector
- LangChain Integration

---

# Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL
- PGVector
- SQLAlchemy
- Alembic
- LangChain
- JWT Auth

---

# Project Structure

app/
├── api/
├── auth/
├── core/
├── db/
├── models/
├── schemas/
├── services/
├── scripts/
└── main.py

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository_url>
cd backend

## 2. Create Virtual Environment

# MAC/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

## 3. Install Dependencies
pip install -r requirements.txt

## 4. PostgreSQL Setup
# Create database:
CREATE DATABASE rag_healthcare;
# Enable pgvector
CREATE EXTENSION vector;

## 5. Run Database Migrations
alembic upgrade head

## 6. Seed Test Users
python -m app.scripts.seed_users

# Default Users:
| Role   | Email                                           | Password  |
| ------ | ----------------------------------------------- | --------- |
| Admin  | [admin@example.com](mailto:admin@example.com)   | admin123  |
| Doctor | [doctor@example.com](mailto:doctor@example.com) | doctor123 |

## 7. Run Application
uvicorn app.main:app --reload

# Backend will run on
http://localhost:8000

# Swagger Docs
http://localhost:8000/docs
