from fastapi import FastAPI
from . import models, routes
from .database import engine, check_and_populate_db
from pathlib import Path
import yaml
from .ml import ml_routes 
from .config import api_description, servers

# Cria as tabelas no banco
models.Base.metadata.create_all(bind=engine)

# Caminho do arquivo YAML
OPENAPI_YAML_PATH = Path(__file__).parent / "openapi_custom.yaml"

if not OPENAPI_YAML_PATH.exists():
    raise FileNotFoundError(f"Arquivo de documentação {OPENAPI_YAML_PATH} não encontrado.")

# Carregar YAML customizado
with open(OPENAPI_YAML_PATH, "r", encoding="utf-8") as f:
    custom_openapi = yaml.safe_load(f)

# Criar instância principal da API
app = FastAPI(
    title=custom_openapi.get("info", {}).get("title", "API"),
    version=custom_openapi.get("info", {}).get("version", "0.1.0"),
    description=custom_openapi.get("info", {}).get("description", ""),
    docs_url=None,  # Desativar docs padrão
    redoc_url=None  # Desativar Redoc padrão
)

# Popula o banco no startup
@app.on_event("startup")
def on_startup():
    check_and_populate_db()

# Inclui as rotas da API e da documentação
app.include_router(routes.router)
