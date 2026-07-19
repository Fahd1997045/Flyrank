# Task API

A small in-memory CRUD API for managing a to-do list. Built with Python and
FastAPI as part of Week 2's "Build your first CRUD API" assignment.

No database — tasks live only in memory and are lost when the server
restarts (see "The mortality experiment" note at the bottom).

## Install & run

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then visit `http://localhost:8000` in your browser, or use the interactive
docs at `http://localhost:8000/docs`.

## Endpoints

| Method | Path            | Meaning                          | Success | Errors |
|--------|-----------------|-----------------------------------|---------|--------|
| GET    | `/`             | API info                          | 200     | —      |
| GET    | `/health`       | Health check                      | 200     | —      |
| GET    | `/tasks`        | List all tasks                    | 200     | —      |
| GET    | `/tasks/{id}`   | Get one task                      | 200     | 404    |
| POST   | `/tasks`        | Create a task (`{"title": "..."}`)| 201     | 400    |
| PUT    | `/tasks/{id}`   | Update a task's title/done        | 200     | 400, 404 |
| DELETE | `/tasks/{id}`   | Delete a task                     | 204     | 404    |

## Example request

```
$ curl -i http://localhost:8000/tasks/1
HTTP/1.1 200 OK
date: Sun, 19 Jul 2026 16:56:52 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

## Swagger UI

Full interactive docs, with a working "Try it out" for every endpoint, live
at `/docs` (FastAPI generates this automatically from the code).

![Swagger UI screenshot](swagger-screenshot.png)

<!-- Replace the line above with your own screenshot of /docs before you
     submit — take it after you've run through the full CRUD cycle there. -->

## The mortality experiment

<!-- Do this yourself: create a task, restart the server (Ctrl+C, then
     re-run the uvicorn command), then GET /tasks again. Write 1-2 sentences
     here about what you saw and why — this is the whole point of Week 3. -->
