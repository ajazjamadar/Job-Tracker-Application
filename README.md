Job Application Tracker

Quickstart

1. Create a virtualenv called `.venv` in the project root and activate it (PowerShell):

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

2. Install deps:

```powershell
pip install -r requirements.txt
```

3. Run:

```powershell
python wsgi.py
```

Project layout

- `app/` — main Flask package. See `routes.py`, `models.py`, `auth.py`, `api.py`.
- `config.py` — configuration.
- `wsgi.py` — development entrypoint.

Notes: This scaffold uses a simple in-memory model in `app/models.py` for easy local development. Replace with a DB for persistence.




