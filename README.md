# Contact Manager Messager
**Updated**: April 2026

Contact Manager Messager is a legacy full-stack productivity tool I built in 2016 to automate contact import and individualized email outreach from exported datasets. It demonstrates pragmatic integration across Flask, SQLite, frontend UI flows, and SMTP-based messaging, while also showing clear opportunities for modernization around security, testability, and Python 3 compatibility.
I built it as a practical way to reduce the manual work involved in taking exported contacts, loading them into a system, selecting recipients, and sending one-by-one emails with a shared message and attachment.

In spite that this whole set of activities can be solved with a mere Thunderbird/mailbox plug-in, nowadays; at the time I though the exercise would be a practical stretch of skill.

## Scope

The application focuses on a narrow but useful workflow:

1. Log in with SMTP credentials.
2. Upload a CSV file containing contacts.
3. Import those contacts into a per-user SQLite database.
4. Retrieve and display the imported contacts in the UI.
5. Select recipients.
6. Send individualized emails with a shared subject, body, and attachment.

The repository also includes a later standalone script, [`send_emails_massive.py`](/send_emails_massive.py), which explores the same outreach problem from a more direct CLI/pandas approach.

## What is does

- Solves a real workflow end to end instead of stopping at a toy CRUD example.
- Connects several concerns in one system: CSV ingestion, local persistence, session state, REST endpoints, frontend selection, and SMTP delivery.
- Uses a pragmatic architecture for the problem size: Flask for the web layer, SQLite for persistence, AngularJS for the UI.
- Separates responsibilities reasonably well for a prototype, with import, contact retrieval, and messaging logic split across controllers and support classes.
- Handles duplicate contacts at import time by attempting insert first and then update on unique constraint.
- Creates isolated SQLite databases per user email, which is a practical way to separate contact sets in a simple local deployment model.
- Includes both a browser-based workflow and a later script-based workflow, showing iteration over time rather than a single static implementation.

## Current Architecture

- Backend: Flask app in [`webservices.py`](/webservices.py)
- Core logic: import, DAO, contact entity, and mail sending in [`backend.py`](/backend.py)
- Frontend: AngularJS + jQuery in [`static/js/app.js`](/static/js/app.js)
- Views: Jinja templates in [`templates/`](/templates)
- Persistence: SQLite databases generated per logged-in user
- Deployment intent: Gunicorn via [`Procfile`](/Procfile)

## Tech Stack

- Python
- Flask
- AngularJS 1.x
- jQuery
- Bootstrap
- SQLite
- SMTP

## What It Does Not Do

- It is not a full CRM.
- It does not provide campaign analytics, bounce tracking, unsubscribe management, or deliverability monitoring.
- It does not integrate directly with LinkedIn APIs, Gmail APIs, or modern mail provider SDKs.
- It does not provide role-based access control, user registration, multi-tenant administration, or production-grade account management.
- It does not include background job processing, queueing, or rate-aware email scheduling.
- It does not normalize many different CSV schemas robustly; the import logic is tied to a specific LinkedIn-export-style column layout.

## What Is Lacking And Should Be Addressed

This is the main technical debt I would address if I decided to move it forward as production-ready software.

### 1. Python/runtime modernization

The core application code is written in a Python 2 style, while the bundled local virtual environment points to Python 3.9. The current codebase contains Python 2-only constructs such as `print` statements without parentheses and `unicode(...)`, so it does not run cleanly under modern Python without refactoring.
(Honestly, in 2016, I was more of a Java programmer than a Python one, and this project shows it)

### 2. Security hardening

- SMTP credentials are kept in the Flask session.
- The Flask secret key is hardcoded in source.
- The app accepts file uploads with only basic extension checks.
- There is no strong validation, encryption strategy, or secrets management.

This is a prototype, not a secure production system.
However, these matters are interesting to have into the radar since, in a real production scenario they aren't acceptable.

### 3. Test reliability

There is a test file, [`tests.py`](/tests.py), but it is incomplete and not a dependable safety net. Some tests reference commented-out code paths or variables that are never defined. It needs more work, and this is not something I plan to prioritize anytime soon.

### 4. Frontend modernization

The frontend relies on AngularJS 1.x, jQuery, and Bower-managed assets. That stack was reasonable when the project was created (2016), but today it is legacy technology and would benefit from modernization.

### 5. Operational robustness

- No asynchronous sending pipeline
- No retry or dead-letter mechanism
- No structured audit trail for mail outcomes
- No rate limiting or throttling strategy
- No containerization or reproducible local bootstrap

It's simple and straight to the point prototype.

## TO-DOs

The next practical improvements, (in case one day I'm interested in implementing it):

- Port the backend fully to Python 3.
- Replace plaintext/session credential handling with environment-based secrets and safer auth flows.
- Introduce schema validation for uploads and REST payloads.
- Add automated tests for import, contact retrieval, and email orchestration.
- Replace AngularJS/Bower dependencies with a modern frontend stack or a simpler server-rendered UI.
- Add a proper mail delivery abstraction with retries, logging, and provider adapters.
- Add Docker and a reproducible local development setup.

## Notes
I consider this repository a code sample / legacy prototype rather than a ready-to-run production app.
My intention is to show some history about my first few approachs to python.
Since I'm a professional software developer since the turn of the century, the amount of free of NDA code I've produced is scarce.
This, is one of the few samples that aren't miss in the sands of time, and shows how I worked with a new technology, ten years ago.
Good for archeological means, and getting to know me.
Not anymore for any practical use.



