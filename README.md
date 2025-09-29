# 🧠 NLP Query Engine

A Natural Language Processing (NLP)-powered query engine that allows users to:
- Connect to a relational database.
- Upload supporting documents for context.
- Ask natural language questions and get **SQL queries + answers**.

This project was built as part of a technical assignment.

---

## 🚀 Features
- **Database Connectivity**: Connect to SQLite (or other databases) using a connection string.
- **Document Upload**: Upload `.txt` files to enhance query responses.
- **NLP Engine**: Convert natural language questions into SQL queries.
- **REST API**: Powered by **FastAPI**.
- **Frontend UI**: Simple interface (HTML + JS) to test queries.

---

## 🛠 Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, Sentence-Transformers
- **Frontend**: HTML, Vanilla JavaScript
- **Database**: SQLite
- **Other Tools**: Uvicorn, Pandas, Hugging Face models

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone git@github.com:Sanvi09Kulkarni/nlp-query-engine.git
cd nlp-query-engine
