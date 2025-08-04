from fastapi import FastAPI
from . import models, routes
from .database import engine, check_and_populate_db
from .auth import router as auth_router

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API de Consulta de Livros",
    version="0.1.0",
    description="Uma API para consulta de dados de livros extraídos via web scraping.",
)

# Populando o banco de dados na inicialização
@app.on_event("startup")
def on_startup():
    check_and_populate_db() 

app.include_router(routes.router)
app.include_router(auth_router, prefix="/api/v1/auth")