from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
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
    Retorna uma lista de TODOS os livros disponíveis na base de dados.
    """
    books = services.get_all_books(db)
    return books


# Endpoint para buscar livros por titulo e/ou categoria
@router.get(
    "/books/search", 
    response_model=List[schemas.BookSchema], 
    summary="Busca livros por título e/ou categoria",
    tags=["Books"]
)
def search_for_books(title: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Busca livros que correspondam a um título e/ou categoria.
    - Pelo menos um dos parâmetros (`title` ou `category`) deve ser fornecido.
    - A busca por título é por similaridade e não diferencia maiúsculas de minúsculas.
    - A busca por categoria é exata.
    """
    if not title and not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Forneça pelo menos um critério de busca: 'title' ou 'category'."
        )
    return services.search_books(db, title=title, category=category)


# Endpoint para obter detalhes de um livro específico pelo ID
@router.get(
    "/books/{book_id}",
    response_model=schemas.BookSchema,
    summary="Retorna um livro específico pelo ID",
    tags=["Books"]
)
def get_book_details(book_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes completos de um livro específico com base no seu ID.
    """
    return services.get_book_by_id(db, book_id=book_id)


# Endpoint para listar todas as categorias de livros
@router.get(
    "/categories", 
    response_model=schemas.CategoryListSchema, 
    summary="Lista todas as categorias de livros",
    tags=["Categories"]
)
def list_categories(db: Session = Depends(get_db)):
    """
    Retorna uma lista com todas as categorias de livros únicas disponíveis.
    """
    categories_list = services.get_all_categories(db)
    return {"categories": categories_list}