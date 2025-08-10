from fastapi import FastAPI
from . import models, routes
from .database import engine, check_and_populate_db 
from .ml import ml_routes 
from .config import api_description, servers

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="FIAP ML Tech Challenge 1 - API com Web Scraping",
    version="0.1.0",
    description=api_description,
    servers=servers,
)

# Popula o banco de dados na inicialização
@app.on_event("startup")
def on_startup():
    check_and_populate_db() 

# Inclui os roteadores na aplicação
app.include_router(routes.router)
app.include_router(ml_routes.router)

    