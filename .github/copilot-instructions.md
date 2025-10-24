# Copilot instructions for Job Application Tracker

Overview

This is a small Flask web app used to track job applications. The app lives in the `app/` package and is designed for local development with a small in-memory model (`app/models.py`). Replace the in-memory store with a DB-backed model when adding persistence.

Key files

- `app/__init__.py` — creates the Flask `app` instance and loads `Config`.
- `app/routes.py` — UI routes and form handling (renders templates in `app/templates/`)
- `app/models.py` — simple Application model and `applications` in-memory list
- `app/auth.py` — tiny in-process user store for demo auth
- `app/api.py` — JSON returns for programmatic access (see `application_list()`)
- `app/forms.py` — WTForms-based forms used by views
- `config.py` — configuration entry, uses `SECRET_KEY` and `FLASK_DEBUG`
- `wsgi.py` — development entrypoint, runs `app`.

Project conventions and patterns

- Single-process, in-memory data: `app/models.py` uses `applications` list and `Application` objects; code that mutates data appends/edits objects directly. Avoid introducing async or multi-process assumptions without switching to a proper DB.
- Templates are under `app/templates/`. Route functions in `app/routes.py` call `render_template()` with either `applications` or a single `application`.
- Minimal auth: `app/auth.py` stores `users` in-memory using `werkzeug.security` hashes. Any persistent auth work should migrate this to a DB (e.g., Flask-Login + SQLAlchemy).
- Forms: `app/forms.py` uses Flask-WTF; views currently use plain `request.form` for simplicity. If adding CSRF or form objects, prefer wiring `FlaskForm` classes and passing them into templates.

How to run locally (developer workflow)

1. Create and activate venv in the project root (PowerShell):

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app for development:

```powershell
python wsgi.py
# or set FLASK_APP and use flask run
$env:FLASK_APP = 'wsgi.py'; flask run
```

Patterns to follow when changing behavior

- When replacing `applications` with a DB, update every import site that reads/writes `applications` (routes, api, templates). Prefer adding a small data access layer in `app/models.py` exposing `list_applications()`, `get_application(id)`, `save_application(app)` to keep route code minimal.
- Keep templates simple and rely on route-provided objects; avoid complex logic in templates.

Examples

- To return JSON for API consumers, follow `app/api.py`'s `application_list()` which maps `Application.to_dict()`.
- To add a new route that mutates data, append to `applications` and redirect to list views (see `routes.new_application`).

Notes for AI agents

- Focus changes within `app/` unless you're adding infra (Docker, CI). Small changes are best implemented by editing `routes.py`, `models.py`, `templates/` together.
- Do not assume persistence across runs; if a feature requires persistence, explicitly add a DB migration plan and wire it into `config.py` and `wsgi.py`.
- Use the in-repo `README.md` for quickstart steps and mirror any run commands you add there.

If anything above is unclear or you'd like more examples (database migration, unit tests, or adding Flask-Login integration), ask and I'll expand the instructions.




