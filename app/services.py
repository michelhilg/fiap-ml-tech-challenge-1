from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from . import models
import logging

def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    """
    Busca todos os livros no banco de dados com tratamento de erros.
    - Lança um erro 404 se nenhum livro for encontrado.
    - Lança um erro 500 em caso de falha na consulta ao banco de dados.
    """
    try:
        books = db.query(models.Book).offset(skip).limit(limit).all()

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