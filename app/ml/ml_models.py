from sqlalchemy import Column, Integer, Float, JSON
from ..database import Base

class BookFeature(Base):
    """
    Modelo SQLAlchemy para a tabela 'ml_data'.
    Armazena os dados pré-processados e prontos para ML.
    """
    __tablename__ = "ml_data"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer) 
    price = Column(Float)
    rating_numeric = Column(Integer)
    availability_numeric = Column(Integer)
    # Armazena as colunas de categoria (one-hot encoded) como um objeto JSON
    category_features = Column(JSON)