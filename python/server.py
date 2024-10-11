from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import main
import transactions

app = FastAPI()

class Transaction(BaseModel):
    date: str
    amount: float
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/calculate_budget")
def calculate_budget(user):
    data = main.create_datasets(user)
    smart_budget = main.calculate_smart_budget(data)
    return {f"Your smart budget is ${smart_budget}"}


print(calculate_budget("josesm82@gmail.com"))









