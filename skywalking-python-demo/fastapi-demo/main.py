from typing import Union

from fastapi import FastAPI
from pymilvus import connections, db

connections.connect(host="127.0.0.1", port="19530")

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World", "foo": etcd.get("foo")}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/milvus/create_db")
def create_db():
    db.create_database("test_db")
    return {"status": "success"}
