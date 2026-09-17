from fastapi import FastAPI

app = FastAPI(
    title="RH Prediction",
    description="API qui permet d'evaluer le risque d'attrition",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"message": "OK"}

@app.post("/pedict")
def predict_attrition():
    return {"message" : "predction"}