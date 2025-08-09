from pydantic import BaseModel 
from typing import List, Dict, Any

class BookFeatureSchema(BaseModel):
    """
    Schema para a resposta do endpoint /features
    """
    id: int
    book_id: int
    price: float
    rating_numeric: int
    availability_numeric: int
    category: str # A categoria é retornada como string

    class Config:
        from_attributes = True

class TrainingDataResponseSchema(BaseModel):
    """
    Schema para a resposta do endpoint /training-data
    """
    training_dataset: List[BookFeatureSchema]

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