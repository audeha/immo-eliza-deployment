from fastapi import FastAPI
from pydantic import BaseModel
import csv
from predict import predict

app = FastAPI()

class Item(BaseModel):
    nbr_frontages: int
    fl_terrace: bool
    equipped_kitchen: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def create_item(item: Item):
    with open("csv_file.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(item.model_dump().keys())
        writer.writerow(item.model_dump().values())
    
    return predict("csv_file.csv")
