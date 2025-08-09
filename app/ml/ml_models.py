from sqlalchemy import Column, Integer, Float, String
from ..database import Base

class BookFeature(Base):
    """
    Modelo SQLAlchemy para a tabela 'ml_data'.
    Armazena os dados pré-processados e prontos para ML.
    """
    __tablename__ = "ml_data"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer) #FK
    price = Column(Float)
    rating_numeric = Column(Integer)
    availability_numeric = Column(Integer)
    category = Column(String)