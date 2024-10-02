from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Transaction(BaseModel):
    date: str
    amount: float
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/calculate_budget")
def calculate_budget(transactions: List[Transaction]):
    return {"Message to show to the user based on his expenses"}

