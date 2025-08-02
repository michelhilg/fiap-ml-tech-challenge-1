from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from typing import List
import os

from . import services, schemas
from .database import get_db

# Cria um roteador para agrupar os endpoints de livros
router = APIRouter(
    prefix="/api/v1"
)

# Endpoint de Health Check
DB_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.db')

@router.get(
    "/health",
    summary="Verifica a saúde da API e conexão com o banco de dados",
    tags=["Monitoring"]
)
def health_check(response: Response):
    if not os.path.exists(DB_FILE_PATH):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"api_status": "ok", "database_status": "not connected"}
    return {"api_status": "ok", "database_status": "ok"}


# Endpoint para listar todos os livros 
@router.get(
    "/books",
    response_model=List[schemas.BookSchema],
    summary="Lista todos os livros",
    tags=["Books"] 
)
def list_books(db: Session = Depends(get_db)):
    """
    Retorna uma lista de todos os livros disponíveis na base de dados.
    A resposta é paginada por padrão (primeiros 100 livros).
    """
    books = services.get_all_books(db)
    return books