from sqlalchemy.orm import Session
from fastapi import HTTPException
import re
import logging
from typing import List, Dict, Any
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from .. import models
from . import ml_schemas as schemas
from . import ml_models

def process_and_save_features(db: Session) -> List[ml_models.BookFeature]:
    """
    Processa os dados da tabela 'books', cria features numéricas e salva o resultado na tabela 'ml_data'.
    - Lança um erro 404 se não encontrar livros na tabela 'books'.
    - Lança um erro 500 se ocorrer um erro ao salvar os dados processados.
    """
    logging.info("Iniciando o processo de criação de features na tabela 'ml_data'...")
    
    all_books = db.query(models.Book).all()
    if not all_books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado na tabela 'books' para processar.")

    df = pd.DataFrame([book.__dict__ for book in all_books])

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['rating_numeric'] = df['rating'].map(rating_map).fillna(0).astype(int)
    df['availability_numeric'] = df['availability'].str.extract(r'(\d+)', expand=False).fillna(0).astype(int)

    features_df = df[['id', 'price', 'rating_numeric', 'availability_numeric', 'category']]

    try:
        db.query(ml_models.BookFeature).delete()
        logging.info("Tabela 'ml_data' limpa com sucesso.")

        features_to_save = []
        for _, row in features_df.iterrows():
            feature_instance = ml_models.BookFeature(
                book_id=int(row['id']),
                price=float(row['price']),
                rating_numeric=int(row['rating_numeric']),
                availability_numeric=int(row['availability_numeric']),
                category=str(row['category'])
            )
            features_to_save.append(feature_instance)
        
        db.add_all(features_to_save)
        db.commit()
        logging.info(f"{len(features_to_save)} registros de features foram salvos em 'ml_data'.")
        
        return db.query(ml_models.BookFeature).all()

    except Exception as e:
        db.rollback()
        logging.error(f"Erro ao salvar features no banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Falha ao salvar features processadas.")

def get_encoded_training_data(db: Session) -> List[Dict[str, Any]]:
    """
    Lê os dados da tabela 'ml_data', aplica One-Hot Encoding na categoria e retorna o dataset final pronto para treinamento.
    - Lança um erro 404 se não encontrar dados na tabela 'ml_data'.
    """
    logging.info("Iniciando a preparação do dataset de treinamento com One-Hot Encoding...")
    
    features_from_db = db.query(ml_models.BookFeature).all()
    if not features_from_db:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado na tabela 'ml_data'. Execute o endpoint /features primeiro.")

    df = pd.DataFrame([f.__dict__ for f in features_from_db])
    
    # Remover colunas desnecessárias do SQLAlchemy e a chave primária da tabela de features
    df = df.drop(columns=['_sa_instance_state', 'id'])

    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    category_encoded = encoder.fit_transform(df[['category']])
    category_df = pd.DataFrame(category_encoded, columns=encoder.get_feature_names_out(['category']))

    # Juntar os dataframes, removendo a coluna original de categoria
    final_df = df.drop(columns=['category']).join(category_df)
    
    # Converter o dataframe final para uma lista de dicionários para a resposta JSON
    return final_df.to_dict(orient='records')

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