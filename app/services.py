from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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