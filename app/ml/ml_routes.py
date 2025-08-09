from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import ml_services as services, ml_schemas as schemas 
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/ml",
    tags=["Machine Learning"]
)

@router.get("/features", response_model=List[schemas.BookFeatureSchema], summary="Dados formatados como features")
def get_features(db: Session = Depends(get_db)):
    return services.get_books_as_features(db)

@router.get("/training-data", response_model=schemas.TrainingDataSchema, summary="Dataset completo para treinamento")
def get_training_data(db: Session = Depends(get_db)):
    dataset = services.get_training_dataset(db)
    return {"dataset": dataset}

@router.post("/predictions", response_model=schemas.PredictionResponseSchema, summary="Endpoint para receber predições")
def create_prediction(request: schemas.PredictionRequestSchema):
    return services.make_prediction(request)