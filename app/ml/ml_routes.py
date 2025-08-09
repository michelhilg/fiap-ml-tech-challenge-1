from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import ml_services as services
from . import ml_schemas as schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/ml",
    tags=["Machine Learning"]
)

@router.get(
    "/features", 
    response_model=List[schemas.BookFeatureSchema], 
    summary="Processa e salva features básicas"
)
def get_and_save_features(db: Session = Depends(get_db)):
    """
    Processa dados da tabela 'books', cria features numéricas, salva o
    resultado na tabela 'ml_data' e retorna os dados salvos.
    A coluna 'category' permanece como string.
    """
    return services.process_and_save_features(db)

@router.get(
    "/training-data", 
    response_model=schemas.TrainingDataResponseSchema, 
    summary="Dataset pré-processado para treinamento")
def get_training_data_route(db: Session = Depends(get_db)):
    """
    Lê os dados da tabela 'ml_data' e os retorna.
    """
    dataset = services.get_training_data(db)
    return {"training_dataset": dataset}

@router.post(
    "/predictions", 
    response_model=schemas.PredictionResponseSchema, 
    summary="Endpoint para receber predições"
)
def create_prediction(request: schemas.PredictionRequestSchema):
    """Endpoint para receber dados de entrada e retornar uma predição simulada."""
    return services.make_prediction(request)