from fastapi import FastAPI
from . import models, routes
from .database import engine

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API de Consulta de Livros",
    version="0.1.0",
    description="Uma API para consulta de dados de livros extraídos via web scraping.",
)

app.include_router(routes.router)