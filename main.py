from fastapi import FastAPI
from pydantic import BaseModel
import csv
import pandas as pd
import joblib
import json

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

    artifacts = joblib.load("models/artifacts.joblib")

    # Unpack the artifacts
    num_features = artifacts["features"]["num_features"]
    fl_features = artifacts["features"]["fl_features"]
    cat_features = artifacts["features"]["cat_features"]
    imputer = artifacts["imputer"]
    enc = artifacts["enc"]
    model = artifacts["model"]

    # Extract the used data

    data = pd.read_csv("csv_file.csv")

    data = data.to_json(orient='records')
    data = json.loads(data)[0]
    data = data.reshape(1,-1)

    # Apply imputer and encoder on data
    transformed_data = {}
    for feature in num_features:
        transformed_data[feature] = imputer.transform([data[feature]])[0]
    for feature in cat_features:
        transformed_data[feature] = data[feature]
    transformed_data = pd.DataFrame(transformed_data, index=[0])

    data_cat = enc.transform(transformed_data[cat_features]).toarray()

    # Combine the numerical and one-hot encoded categorical columns
    data = pd.concat(
        [
            transformed_data[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(data_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    # Make predictions
    predictions = model.predict(data)
    return predictions
