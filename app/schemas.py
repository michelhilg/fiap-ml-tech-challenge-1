from pydantic import BaseModel
from typing import List

# Schema existente para um único livro
class BookSchema(BaseModel):
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

# Schema para a lista de categorias
class CategoryListSchema(BaseModel):
    categories: List[str]