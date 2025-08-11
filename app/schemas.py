from pydantic import BaseModel
from typing import List, Dict

class BookSchema(BaseModel):
    """ Schema para um único livro. """
    id: int
    title: str
    price: float
    rating: str
    availability: str
    category: str
    image_url: str

    # Configuração para permitir que o Pydantic leia dados de objetos ORM
    class Config:
        from_attributes = True

class CategoryListSchema(BaseModel):
    """ Schema para a lista de categorias de livros. """
    categories: List[str]

class OverviewStatsSchema(BaseModel):
    """ Schema para as estatísticas gerais da coleção. """
    total_books: int
    average_price: float
    rating_distribution: Dict[str, int]

class CategoryStatItemSchema(BaseModel):
    """ Schema para as estatísticas de uma única categoria. """
    category: str
    book_count: int
    average_price: float
    min_price: float
    max_price: float
    average_rating: float

class CategoryStatsSchema(BaseModel):
    """ Schema para a lista de estatísticas de todas as categorias. """
    stats: List[CategoryStatItemSchema]

class TokenSchema(BaseModel):
    """ Schema para o token de autenticação. """
    access_token: str
    token_type: str
