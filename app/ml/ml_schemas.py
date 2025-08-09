from pydantic import BaseModel 
from typing import List, Dict, Any

class BookFeatureSchema(BaseModel):
    """
    Schema para os dados de um livro formatados como features para um modelo.
    """
    id: int
    price: float
    rating_numeric: int
    availability_numeric: int
    category: str

class TrainingDataSchema(BaseModel):
    """
    Schema para o dataset de treinamento completo.
    """
    dataset: List[Dict[str, Any]]

class PredictionRequestSchema(BaseModel):
    """
    Schema para a requisição de predição.
    """
    price: float
    category: str
    availability_numeric: int

class PredictionResponseSchema(BaseModel):
    """
    Schema para a resposta da predição.
    """
    predicted_rating: str
    confidence_score: float