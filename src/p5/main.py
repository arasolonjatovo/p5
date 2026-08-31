from fastapi import FastAPI, status, HTTPException
from .model import ml_service
from .schemas import EmployeeDataInput, PredictionOutput

app = FastAPI(
    title="RH Prediction",
    description="API qui permet d'evaluer le risque d'attrition",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Helath"])
def health_check():
    return {"status": "healthy", "model_loaded": ml_service.pipeline is not None}

@app.post("/predict", response_model=PredictionOutput, status_code=status.HTTP_200_OK, tags=["Inference"])
def predict_attrition(payload: EmployeeDataInput):
    """Endpoint effectuant une prédiction sur les données d'un employé."""
    try:
        prediction, probability = ml_service.predict(payload)
        return PredictionOutput(
            prediction=prediction,
            probabilite_attrition=probability,
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne lors de la prédiction : {str(e)}"
        )