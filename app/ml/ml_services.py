from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
import re
import logging
from .. import models
from . import ml_schemas as schemas 

def get_books_as_features(db: Session) -> List[schemas.BookFeatureSchema]:
    """
    Busca todos os livros e os transforma em um formato de features para ML.
    """
    all_books = db.query(models.Book).all()
    if not all_books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado para gerar features.")

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    
    feature_list = []
    for book in all_books:
        availability_match = re.search(r'\((\d+) available\)', book.availability)
        availability_numeric = int(availability_match.group(1)) if availability_match else 0
        
        feature_list.append(schemas.BookFeatureSchema(
            id=book.id,
            price=book.price,
            rating_numeric=rating_map.get(book.rating, 0),
            availability_numeric=availability_numeric,
            category=book.category
        ))
    
    return feature_list

def get_training_dataset(db: Session) -> List[dict]:
    """
    Retorna o dataset completo, pronto para ser usado em treinamento.
    """
    all_books = db.query(models.Book).all()
    if not all_books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado para gerar dataset de treino.")
    
    return [book.__dict__ for book in all_books]

def make_prediction(request_data: schemas.PredictionRequestSchema) -> schemas.PredictionResponseSchema:
    """
    Simula uma predição com base nos dados de entrada.
    """
    logging.info(f"Recebida requisição de predição: {request_data}")
    
    if request_data.price > 50.00:
        predicted_rating = "Five"
        confidence = 0.95
    elif request_data.category == "Mystery":
        predicted_rating = "Four"
        confidence = 0.88
    else:
        predicted_rating = "Three"
        confidence = 0.75

    return schemas.PredictionResponseSchema(
        predicted_rating=predicted_rating,
        confidence_score=confidence
    )