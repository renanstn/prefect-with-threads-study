import random
import time

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/random_value")
def random_value():
    time.sleep(0.5)
    return {"value": random.randint(0, 100)}
