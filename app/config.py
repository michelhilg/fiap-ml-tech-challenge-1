# Descrição detalhada da API para o Swagger UI, com suporte a Markdown
api_description = """
 
### API RESTful para utilizações de dados obtidos via web scraping de https://books.toscrape.com

### Principais funcionalidades
- **Scraping de livros**: coleta automática de dados de livros do site especificado.
- **Autenticação via JWT (Bearer Token)** para acesso a rotas protegidas.
- **Consulta de livros**: listagem, busca por ID, título/categoria, faixa de preço e mais bem avaliados.
- **Estatísticas** gerais da coleção e detalhadas por categoria.
- **Endpoints ML-Ready**: rotas dedicadas para obter dados formatados para treinamento de modelos.
- **Health-check** para monitoramento da saúde da API.

---

### Instruções de Uso

#### 0. Pré-requisito: Fonte de Dados
A API popula seu banco de dados a partir do arquivo `data/books.csv` na primeira inicialização. Antes de rodar a API localmente, garanta que este arquivo exista.
- Para criar ou atualizar o arquivo, execute o script de scraping: `python scripts/scraper.py`

#### 1. Selecione um Servidor
No menu suspenso "Servers" no topo desta página, escolha o ambiente que deseja testar:
- **Produção**: `https://fiap-ml-tech-challenge-1-nine.vercel.app` - Servidor de deploy na Vercel.
- **Local**: `http://127.0.0.1:8000` - Servidor para execução local.

#### 2. Autenticação
Para acessar os endpoints protegidos (marcados com um 🔒), você precisa de um token. Utilize o endpoint `POST /api/v1/login` com as seguintes credenciais de teste:
- **Username**: `admin`
- **Password**: `admin123`

Agora você consegue utilizar seu `Bearer <seu_token>` gerado para acessar as rotas protegidas.

De forma opcional, também se pode realizar o login via **Swagger UI** clicando no botão `Authorize` e inserindo as credenciais acima.
"""

# Define os servidores disponíveis para a documentação
servers = [
    {
        "url": "https://fiap-ml-tech-challenge-1-nine.vercel.app",
        "description": "Produção - Vercel server"
    },
    {
        "url": "http://127.0.0.1:8000",
        "description": "Execução local"
    }
]