from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, case
from fastapi import HTTPException, status
from typing import List, Optional
from . import models
import logging

def get_all_books(db: Session) -> List[models.Book]:
    """
    Busca todos os livros no banco de dados com tratamento de erros.
    - Lança um erro 404 se nenhum livro for encontrado.
    - Lança um erro 500 em caso de falha na consulta ao banco de dados.
    """
    try:
        books = db.query(models.Book).all()
        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro foi encontrado na base de dados."
            )
        return books

    except SQLAlchemyError as e:
        logging.error(f"Erro no banco de dados ao buscar livros: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao acessar a base de dados."
        )
    
def get_book_by_id(db: Session, book_id: int) -> models.Book:
    """
    Busca um único livro pelo seu ID.
    - Lança um erro 404 se o livro não for encontrado.
    - Lança um erro 500 em caso de falha na consulta ao banco de dados
    """
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Livro com ID {book_id} não encontrado."
            )
        return book
    
    except SQLAlchemyError as e:
        logging.error(f"Erro no banco de dados ao buscar livro por ID: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao acessar a base de dados."
        )
    
def search_books(db: Session, title: Optional[str] = None, category: Optional[str] = None) -> List[models.Book]:
    """
    Busca livros por título e/ou categoria.
    - Se nenhum critério for fornecido, retorna todos os livros.
    - Lança um erro 404 se nenhum livro for encontrado com os critérios fornecidos.
    - Lança um erro 500 em caso de falha na consulta ao banco de dados
    """
    try:
        query = db.query(models.Book)

        if title:
            # Usa 'ilike' para uma busca case-insensitive
            query = query.filter(models.Book.title.ilike(f"%{title}%"))
        if category:
            # Busca exata para categoria
            query = query.filter(models.Book.category == category)
        books = query.all()
        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro encontrado com os critérios de busca fornecidos."
            )
        return books
    
    except SQLAlchemyError as e:
        logging.error(f"Erro no banco de dados ao buscar livros: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao acessar a base de dados."
        )
    
def get_all_categories(db: Session) -> List[str]:
    """
    Retorna uma lista de todas as categorias de livros únicas.
    - Lança um erro 404 se nenhuma categoria for encontrada.
    - Lança um erro 500 em caso de falha na consulta ao banco de dados
    """
    try:
        categories_tuples = db.query(models.Book.category).distinct().all()
        categories = [category[0] for category in categories_tuples]

        if not categories:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma categoria encontrada na base de dados."
            )
        return categories
    
    except SQLAlchemyError as e:
        logging.error(f"Erro no banco de dados ao buscar categorias: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao acessar a base de dados."
        )
    
def get_books_by_price_range(db: Session, min_price: float, max_price: float) -> List[models.Book]:
    """ 
    Filtra livros dentro de uma faixa de preço específica. 
    - Lança um erro 404 se nenhum livro for encontrado na faixa de preço.
    - Lança um erro 500 em caso de falha na consulta ao banco de dados.
    """
    try:
        books = db.query(models.Book).filter(models.Book.price.between(min_price, max_price)).all()
        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum livro encontrado na faixa de preço de {min_price} a {max_price}."
            )
        return books
    except SQLAlchemyError as e:
        logging.error(f"Erro no banco de dados ao filtrar por preço: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")

def get_top_rated_books(db: Session) -> List[models.Book]:
    """ 
    Retorna todos os livros com a avaliação máxima ('Five'). 
    - Lança um erro 404 se nenhum livro com avaliação máxima for encontrado.
    - Lança um erro 500 em caso de falha na consulta ao banco de dados.
    """
    try:
        books = db.query(models.Book).filter(models.Book.rating == 'Five').all()
        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro com avaliação máxima foi encontrado."
            )
        return books
    except SQLAlchemyError as e:
        logging.error(f"Erro no banco de dados ao buscar livros mais bem avaliados: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")

def get_general_stats(db: Session) -> dict:
    """ 
    Calcula as estatísticas gerais da coleção de livros.
    - Lança um erro 500 em caso de falha na consulta ao banco de dados.
    """
    try:
        total_books = db.query(models.Book).count()
        if total_books == 0:
            return {"total_books": 0, "average_price": 0.0, "rating_distribution": {}}

        avg_price_query = db.query(func.avg(models.Book.price)).scalar()
        average_price = round(avg_price_query, 2) if avg_price_query else 0.0

        rating_dist_query = db.query(models.Book.rating, func.count(models.Book.rating)).group_by(models.Book.rating).all()
        rating_distribution = {rating: count for rating, count in rating_dist_query}

        return {
            "total_books": total_books,
            "average_price": average_price,
            "rating_distribution": rating_distribution
        }
    except SQLAlchemyError as e:
        logging.error(f"Erro no banco de dados ao calcular estatísticas gerais: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")

def get_category_stats(db: Session) -> List[dict]:
    """ 
    Calcula estatísticas detalhadas para cada categoria, incluindo rating médio. 
    - Lança um erro 500 em caso de falha na consulta ao banco de dados.
    """
    try:
        # Mapeia os ratings de string para número para poder calcular a média
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating_case_statement = case(
            rating_map,
            value=models.Book.rating,
            else_=0  # Define 0 para qualquer rating não mapeado
        )

        stats_query = db.query(
            models.Book.category,
            func.count(models.Book.id).label("book_count"),
            func.avg(models.Book.price).label("average_price"),
            func.min(models.Book.price).label("min_price"),
            func.max(models.Book.price).label("max_price"),
            func.avg(rating_case_statement).label("average_rating") # NOVO CÁLCULO
        ).group_by(models.Book.category).all()

        if not stats_query:
            return []

        # Converte o resultado da query para uma lista de dicionários
        stats_list = [
            {
                "category": row.category,
                "book_count": row.book_count,
                "average_price": round(row.average_price, 2) if row.average_price else 0.0,
                "min_price": row.min_price,
                "max_price": row.max_price,
                "average_rating": round(row.average_rating, 2) if row.average_rating else 0.0 # NOVO CAMPO
            } for row in stats_query
        ]
        return stats_list
    except SQLAlchemyError as e:
        logging.error(f"Erro no banco de dados ao calcular estatísticas por categoria: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")