from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
    