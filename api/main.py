from fastapi import FastAPI, Response, status
import os

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API de Consulta de Livros",
    version="0.1.0",
    description="Uma API para consulta de dados de livros extraídos via web scraping do site books.toscrape.com",
)

# Define o caminho para o arquivo de dados.
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'books.csv')

@app.get(
    "/api/v1/health",
    summary="Verifica a saúde da API",
    description="Retorna o status da aplicação e a conectividade com a fonte de dados (arquivo CSV).",
    tags=["Monitoring"] # Agrupa este endpoint na documentação
)
def health_check(response: Response):
    """
    Endpoint de health check.
    Verifica se a API está no ar e se o arquivo de dados `books.csv` está acessível.
    """
    api_status = "ok"
    data_status = "not connected"
    
    # Verifica se o arquivo de dados existe e está acessível
    if os.path.exists(DATA_FILE_PATH):
        data_status = "ok"
    else:
        # Se o arquivo de dados não for encontrado, o serviço é considerado indisponível.
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
    return {
        "api_status": api_status,
        "data_connectivity": data_status
    }

# Ponto de entrada para rodar com 'python api/main.py' (opcional, para debug)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)