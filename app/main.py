import json
from urllib.request import urlopen

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthy")
def healthy():
    return "healthy"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id * 2, "q": f"{q} x {q}"}


@app.get("/todos/{id}")
def todos(id: int):
    return json.loads(
        urlopen(f"https://jsonplaceholder.typicode.com/todos/{id}").read()
    )
