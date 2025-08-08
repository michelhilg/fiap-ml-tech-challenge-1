from fastapi import APIRouter, Depends, Response, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from . import services, schemas
from .database import get_db
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pathlib import Path
import yaml

# Cria um roteador para agrupar os endpoints de livros
router = APIRouter()


# Caminho do YAML
OPENAPI_YAML_PATH = Path(__file__).parent / "openapi_custom.yaml"

with open(OPENAPI_YAML_PATH, "r", encoding="utf-8") as f:
    custom_openapi = yaml.safe_load(f)

# Rota para retornar o OpenAPI customizado
@router.get("/openapi.json", include_in_schema=False)
async def get_openapi_custom():
    return JSONResponse(content=custom_openapi)

# Rota para exibir o Swagger UI usando o YAML customizado
@router.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=custom_openapi.get("info", {}).get("title", "Documentação da API")
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


# ---- BOOKS

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


# Endpoint para obter melhores livros por avaliação
@router.get(
    "/books/top-rated", 
    response_model=List[schemas.BookSchema], 
    summary="Lista os livros com melhor avaliação", 
    tags=["Books"]
)
def get_top_rated(db: Session = Depends(get_db)):
    """ 
    Retorna uma lista de livros com a avaliação máxima ('Five'). 
    """
    return services.get_top_rated_books(db)


# Endpoint para obter livros por faixa de preço
@router.get(
    "/books/price-range", 
    response_model=List[schemas.BookSchema], 
    summary="Filtra livros por faixa de preço", 
    tags=["Books"])
def get_by_price_range(
    min_price: float = Query(..., gt=0, description="Preço mínimo."),
    max_price: float = Query(..., gt=0, description="Preço máximo."),
    db: Session = Depends(get_db)
):
    """ 
    Filtra livros cujo preço esteja entre `min_price` e `max_price`. 
    """
    if min_price > max_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O preço mínimo não pode ser maior que o máximo.")
    return services.get_books_by_price_range(db, min_price=min_price, max_price=max_price)


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


# --- CATEGORIES

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


# --- ESTATISTICS

# Endpoint para obter estatísticas gerais
@router.get(
    "/stats/overview", 
    response_model=schemas.OverviewStatsSchema, 
    summary="Estatísticas gerais da coleção", 
    tags=["Statistics"])
def get_overview_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas gerais, como total de livros, preço médio e distribuição de avaliações. 
    """
    return services.get_general_stats(db)


# Endpoint para obter estatísticas detalhadas por categoria
@router.get(
        "/stats/categories", 
        response_model=schemas.CategoryStatsSchema, 
        summary="Estatísticas detalhadas por categoria", 
        tags=["Statistics"])
def get_category_stats(db: Session = Depends(get_db)):
    """ Retorna estatísticas detalhadas para cada categoria, como contagem de livros e faixa de preço. """
    stats_list = services.get_category_stats(db)
    return {"stats": stats_list}