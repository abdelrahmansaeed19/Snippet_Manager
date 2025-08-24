## 📌 Snippet Manager API

A Django REST Framework (DRF) based backend system that allows developers to securely store, tag, search, and organize code snippets across different programming languages.
It includes features like authentication, CRUD operations, tagging, search, filtering, ordering, and pagination.

## 🚀 Features

🔑 User Authentication – Register & login users.

📝 Snippet Management – Create, update, delete, and retrieve code snippets.

🏷 Tagging & Categorization – Organize snippets with tags and programming languages.

🔍 Search API – Search snippets by keyword (title, content, language).

📑 Pagination – Control snippet list size with page size options.

🎚 Filtering & Ordering – Filter snippets by language or order by creation date.

✅ Unit Tests – Automated tests for CRUD, search, and pagination.

## 🛠 Tech Stack

Backend Framework: Django 5 + Django REST Framework

Database: SQLite (default, configurable to PostgreSQL/MySQL)

Authentication: DRF Auth (Token / JWT support ready)

Testing: Django unittest

Tools: Django Filters, DRF Pagination, DRF SearchFilter

## 📂 Project Structure

Snippet_Manager/
│

├── snippet_manager/          # Project settings

│   ├── settings.py

│   ├── urls.py

│

├── snippet/                  # Core snippets app

│   ├── models.py             # Snippet model

│   ├── serializers.py        # DRF serializers

│   ├── views.py              # API views

│   ├── urls.py               # App routes

│   └── tests/                # Unit tests

│       └── test_snippets.py

│

├── manage.py

└── README.md


## ⚙️ Installation & Setup

1️⃣ Clone the Repository
```
git clone https://github.com/your-username/snippet-manager.git
cd snippet-manager
```
2️⃣ Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```
3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
4️⃣ Apply Migrations
```
python manage.py migrate
```
5️⃣ Create Superuser
```
python manage.py createsuperuser
```
6️⃣ Run Server
```
python manage.py runserver
```

Server will be running at 👉 http://127.0.0.1:8000/

## 📡 API Endpoints
🔑 Authentication
| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| POST   | `/api/auth/register/` | Register new user |
| POST   | `/api/auth/login/`    | Login user        |

📝 Snippets
| Method | Endpoint              | Description                   |
| ------ | --------------------- | ----------------------------- |
| GET    | `/api/snippets/`      | List all snippets (paginated) |
| POST   | `/api/snippets/`      | Create a new snippet          |
| GET    | `/api/snippets/{id}/` | Retrieve a snippet            |
| PUT    | `/api/snippets/{id}/` | Update a snippet              |
| DELETE | `/api/snippets/{id}/` | Delete a snippet              |

🔍 Search, Filter & Pagination
| Method | Endpoint                | Query Params                                     | Example                                                                                  |
| ------ | ----------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| GET    | `/api/snippets/search/` | `q`, `language`, `ordering`, `page`, `page_size` | `/api/snippets/search/?q=python&language=python&ordering=-created_at&page=1&page_size=2` |

## 📜 License

This project is licensed under the MIT License – feel free to use and modify.
