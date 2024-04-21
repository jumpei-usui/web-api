import json
import os
from urllib.request import urlopen

import boto3
import pymysql
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ENDPOINT = os.environ["ENDPOINT"]
PORT = 3306
USER = os.environ["USER"]
REGION = os.environ["REGION"]
DBNAME = os.environ["DBNAME"]
os.environ["LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN"] = "1"

session = boto3.Session(region_name=REGION)
client = session.client("rds")

token = client.generate_db_auth_token(
    DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION
)

try:
    conn = pymysql.connect(
        host=ENDPOINT,
        user=USER,
        passwd=token,
        port=PORT,
        database=DBNAME,
        ssl_ca="/usr/local/share/ca-certificates/global-bundle.pem",
    )
except Exception as e:
    print("Database connection failed due to {}".format(e))


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


@app.get("/tasks/{id}")
def tasks(id: int):
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM task WHERE task_id={id}""")
    query_results = cur.fetchall()
    return query_results[0][1]
