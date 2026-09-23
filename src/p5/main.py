from datetime import datetime
import json

import joblib
import pandas as pd
from fastapi import FastAPI
from sqlalchemy import text

from p5.database import engine
from p5.schemas import PredictionRequest

app = FastAPI(
    title="GHG Prediction API",
    description="API de prédiction des émissions de gaz à effet de serre",
    version="1.0.0",
)

model = joblib.load("model/gb_pipeline_seattle.pkl")


@app.get("/")
def root():
    return {"message": "API Running"}


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/predict")
def predict(data: PredictionRequest):

    df = pd.DataFrame([data.model_dump()])

    df["BuildingAge"] = datetime.now().year - df["YearBuilt"]

    prediction = float(model.predict(df)[0])

    with engine.begin() as conn:
        building_result = conn.execute(
            text(
                """
                INSERT INTO buildings (
                    "PrimaryPropertyType",
                    "YearBuilt",
                    "NumberofBuildings",
                    "NumberofFloors",
                    "PropertyGFATotal",
                    "TotalGHGEmissions"
                )
                VALUES (
                    :PrimaryPropertyType,
                    :YearBuilt,
                    :NumberofBuildings,
                    :NumberofFloors,
                    :PropertyGFATotal,
                    :TotalGHGEmissions
                )
                RETURNING id
                """
            ),
            {
                **data.model_dump(),
                "TotalGHGEmissions": prediction,
            },
        )

        building_id = building_result.scalar()

        request_result = conn.execute(
            text(
                """
                INSERT INTO ml_requests (
                    building_id,
                    input_data
                )
                VALUES (
                    :building_id,
                    :input_data
                )
                RETURNING id
                """
            ),
            {
                "building_id": building_id,
                "input_data": json.dumps(data.model_dump()),
            },
        )

        request_id = request_result.scalar()

        conn.execute(
            text(
                """
                INSERT INTO ml_predictions (
                    request_id,
                    prediction
                )
                VALUES (
                    :request_id,
                    :prediction
                )
                """
            ),
            {
                "request_id": request_id,
                "prediction": prediction,
            },
        )

    return {
        "building_id": building_id,
        "request_id": request_id,
        "prediction": prediction,
        "building_age": int(df["BuildingAge"].iloc[0]),
    }
