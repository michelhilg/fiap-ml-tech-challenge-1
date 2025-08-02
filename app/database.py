from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import csv
import logging
from . import models

# Configuração do Logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do Banco de Dados
DATABASE_URL = "sqlite:///./data/data.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para popular o banco de dados
def check_and_populate_db():
    """
    Verifica se a tabela 'books' está vazia e, se estiver,
    a popula com os dados do arquivo books.csv.
    """
    db = SessionLocal()
    try:
        if db.query(models.Book).first() is None:
            logging.info("Banco de dados vazio. Iniciando população a partir do CSV...")
            
            csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'books.csv')
            
            if not os.path.exists(csv_path):
                logging.warning(f"Arquivo {csv_path} não encontrado. Nenhum dado foi inserido. Execute o scraper primeiro.")
                return

            with open(csv_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                books_to_add = [
                    models.Book(
                        title=row['title'],
                        price=float(row['price']),
                        rating=row['rating'],
                        availability=row['availability'],
                        category=row['category'],
                        image_url=row['image_url']
                    ) for row in reader
                ]
                
                if books_to_add:
                    db.add_all(books_to_add)
                    db.commit()
                    logging.info(f"{len(books_to_add)} livros foram adicionados ao banco de dados.")
                else:
                    logging.info("CSV encontrado, mas está vazio. Nenhum livro adicionado.")
        else:
            logging.info("O banco de dados já contém dados. Nenhuma ação necessária.")
    finally:
        db.close()