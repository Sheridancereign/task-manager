# Task Manager

A simple, HTMX-driven web application for managing projects and tasks. Built as a technical assignment.

## Features

- Create, update, and delete projects
- Add, edit, and delete tasks within a project
- Prioritize tasks (Low / Medium / High)
- Set deadlines for tasks
- Mark tasks as done
- User authentication — each user only sees their own projects and tasks
- One-page application feel — all actions (add/edit/delete/toggle task) happen via AJAX (HTMX), no full page reloads
- Responsive layout (Bootstrap 5 grid) — works on desktop and mobile

## Tech Stack

- **Backend**: Python 3.13, Django 5.2 (class-based views for all CRUD operations)
- **Frontend**: Bootstrap 5, HTMX, Alpine.js, hyperscript
- **Auth**: django-allauth
- **Database**: PostgreSQL
- **Infrastructure**: Docker, Docker Compose
- **Linting**: ruff, pre-commit

## Project Structure

```
apps/
    accounts/       # user account app (allauth integration point)
    projects/       # Project model, views, forms
    tasks/          # Task model, views, forms
config/
    settings/       # split settings: base / dev / prod
templates/          # Django templates (Bootstrap + HTMX)
static/             # custom CSS and JS
```

Business logic lives in...

Business logic lives in `apps/<app>/forms.py` (validation) and `apps/<app>/views.py` (class-based views,
ownership-restricted querysets via `OwnerQuerysetMixin`).

## Running Locally

### Prerequisites

- Docker and Docker Compose installed

### Steps

1. Clone the repository:

```bash
   git clone <repository-url>
   cd task-manager
```

2. Copy the environment variables example file:

```bash
   cp .env.example .env
```

3. Build and start the containers:

```bash
   docker compose build
   docker compose up -d db
```

4. Run migrations:

```bash
   docker compose run --rm web python manage.py migrate
```

5. Create a superuser (for admin access and initial login):

```bash
   docker compose run --rm web python manage.py createsuperuser
```

6. Start the application:

```bash
   docker compose up
```

7. Open your browser at [http://localhost:8000/projects/](http://localhost:8000/projects/) and log in.

### Linting

```bash
docker compose run --rm web ruff check .
docker compose run --rm web ruff format .
```

Pre-commit hooks (ruff) are configured in `.pre-commit-config.yaml`. To enable them locally:

```bash
pip install pre-commit
pre-commit install
```

## SQL Task

Answers to the SQL task are in [`SQL.md`](./SQL.md).

## Live Demo

<!-- add deployed URL here after deployment -->

## Notes

- Task priority (Low/Medium/High) is set via a dropdown and is independent from manual task ordering in the list.
- Deadlines cannot be set in the past (validated both client-side via `<input type="date">` and server-side in
  `TaskForm.clean_deadline`).
