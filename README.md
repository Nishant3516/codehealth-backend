# CodeHealth Backend

Django backend for the CodeHealth platform.

## Tech Stack

- Python
- Django
- PostgreSQL (planned)

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
python manage.py migrate
python manage.py runserver
```
