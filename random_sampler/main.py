import os
import random

import redis

from fastapi import FastAPI

app = FastAPI()
db = redis.Redis(host=os.environ.get("REDIS_HOST"))

encoded_key = "number".encode("utf-8")

@app.get("/sample")
def sample_numbers():

    db_entries = db.xread("number_stream")
    numbers = [int.from_bytes(entry[1][encoded_key], byteorder="little") for entry in db_entries]
    sample = random.choices(numbers, k=10)

    return {"ten_numbers": sample}


@app.post("/add")
def save_number(integer: int):

    data = {"number": int.to_bytes(integer, byteorder="little", length=4)}

    output_data = {"number": integer}
    db.xadd("number_stream", data)
