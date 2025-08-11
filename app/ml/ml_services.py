from sqlalchemy.orm import Session
from fastapi import HTTPException
import re
import logging
from typing import List, Dict, Any
import pandas as pd
from .. import models
from . import ml_schemas as schemas
from . import ml_models

def process_and_return_features(db: Session) -> List[schemas.BookFeatureSchema]:
    """
    Processa os dados da tabela 'books', cria features numéricas e
    retorna o resultado diretamente, sem salvar no banco de dados.
    """
    logging.info("Iniciando o processo de criação de features em memória...")
    
    all_books = db.query(models.Book).all()
    if not all_books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado na tabela 'books' para processar.")

    df = pd.DataFrame([book.__dict__ for book in all_books])

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['rating_numeric'] = df['rating'].map(rating_map).fillna(0).astype(int)
    
    df['availability_numeric'] = df['availability'].str.extract(r'(\d+)', expand=False).fillna(0).astype(int)

    # Prepara a lista de features para retornar
    feature_list = []
    for _, row in df.iterrows():
        feature_list.append(schemas.BookFeatureSchema(
            id=int(row['id']), # Usamos o ID original do livro
            book_id=int(row['id']),
            price=float(row['price']),
            rating_numeric=int(row['rating_numeric']),
            availability_numeric=int(row['availability_numeric']),
            category=str(row['category'])
        ))
    
    logging.info(f"{len(feature_list)} registros de features processados em memória.")
    return feature_list

def get_training_data(db: Session) -> List[schemas.BookFeatureSchema]:
    """
    Processa as features da mesma forma que o endpoint /features e as retorna.
    Esta função agora atua como um alias para manter a consistência do endpoint.
    """
    logging.info("Chamando a lógica de processamento de features para o dataset de treinamento...")
    return process_and_return_features(db)

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