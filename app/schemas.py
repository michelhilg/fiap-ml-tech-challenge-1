from pydantic import BaseModel

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