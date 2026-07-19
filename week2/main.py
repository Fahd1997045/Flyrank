from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Task API", version="1.0")


# The assignment wants every error shaped as {"error": "..."}.
# FastAPI's defaults use {"detail": "..."} (HTTPException) and a
# verbose list (RequestValidationError), so we override both here.
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    field = first["loc"][-1]
    return JSONResponse(
        status_code=400,
        content={"error": f"Invalid value for '{field}': {first['msg']}"},
    )

# --- Stage 2: in-memory "database" ------------------------------------
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write report", "done": True},
    {"id": 3, "title": "Walk the dog", "done": False},
]
next_id = 4  # simple counter for new task ids


# --- Request body shapes (Pydantic handles validation for us) ----------
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    # min_length=1 means: if title is missing or empty, FastAPI
    # automatically returns a 422 with a clear error — this is our
    # "server never trusts the client" rule from Stage 3.


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None


# --- Stage 1: root and health endpoints --------------------------------
@app.get("/", summary="API info")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/tasks/{id}", "/health"],
    }


@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}


# --- Stage 2: Read ------------------------------------------------------
@app.get("/tasks", summary="List all tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get one task by id")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# --- Stage 3: Create ------------------------------------------------------
@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(new_task: TaskCreate):
    global next_id
    task = {"id": next_id, "title": new_task.title, "done": False}
    tasks.append(task)
    next_id += 1
    return task


# --- Stage 4: Update & Delete --------------------------------------------
@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if update.title is not None:
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
