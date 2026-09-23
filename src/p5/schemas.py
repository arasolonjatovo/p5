from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    PrimaryPropertyType: str = Field(..., example="Hotel")
    YearBuilt: int = Field(..., ge=1800, le=2026)
    NumberofBuildings: float = Field(..., gt=0)
    NumberofFloors: int = Field(..., gt=0)
    PropertyGFATotal: float = Field(..., gt=0)
