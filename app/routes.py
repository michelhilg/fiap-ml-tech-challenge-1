from fastapi import APIRouter, Depends, Response, status, HTTPException, Query, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from . import services, schemas
from .database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from .auth import create_access_token, verify_token, FAKE_USER
import os
from jose import jwt
from .auth import SECRET_KEY, ALGORITHM

# Cria um roteador para agrupar os endpoints de livros
router = APIRouter(
    prefix="/api/v1"
)

# ---- MONITORING

# Endpoint de Health Check
DB_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.db')
@router.get(
    "/health",
    summary="Verifica a saúde da API e conexão com o banco de dados",
    tags=["Monitoring"]
)
def health_check(response: Response):
    """
    Endpoint para verificar a saúde da API e a conexão com o banco de dados.
    Retorna um status 'ok' se a API estiver funcionando e o banco de dados estiver acessível.
    Se o banco de dados não estiver acessível, retorna 'not connected'.
    """
    # Verifica se o arquivo do banco de dados existe
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
    """ 
    Retorna estatísticas detalhadas para cada categoria, como contagem de livros e faixa de preço. 
    """
    stats_list = services.get_category_stats(db)
    return {"stats": stats_list}

# --- AUTHENTICATION

@router.post("/login",
             response_model=schemas.TokenSchema,
             summary="Realiza o login e retorna um token de acesso",
             tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para realizar o login e retornar um token de acesso.
    O token deve ser usado para acessar endpoints protegidos.
    O usuário e senha devem ser passados no corpo da requisição como 'application/x-www-form-urlencoded'.
    """
    if (form_data.username != FAKE_USER["username"] or 
        form_data.password != FAKE_USER["password"]):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh",
             response_model=schemas.TokenSchema,
             summary="Renova o token de acesso",
             tags=["Authentication"])
def refresh_token(authorization: str = Header(...)):
    """
    Endpoint para renovar o token de acesso usando o token atual.
    O token deve ser passado no header Authorization como 'Bearer <token>'.
    """
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        new_access_token = create_access_token({"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")