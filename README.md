# fiap-ml-tech-challenge-1

## API com FastAPI

### Como Executar a API

Para iniciar o servidor da API localmente, certifique-se de que seu ambiente virtual (`venv`) está ativado e as dependências do `requirements.txt` estão instaladas.

Execute o seguinte comando a partir do diretório raiz do projeto:

```bash
uvicorn api.main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`.

### Teste Inicial (Health Check)

Um endpoint de *health check* foi criado para monitorar o status da aplicação e sua conectividade com a fonte de dados.

**Endpoint:** `GET /api/v1/health`

Este endpoint verifica duas condições:

1.  Se a aplicação FastAPI está rodando (`api_status`).
2.  Se o arquivo de dados `data/books.csv` existe e está acessível (`data_connectivity`).

#### Resultado Esperado

**Cenário de Sucesso (Tudo OK):**

Se o arquivo `books.csv` existir, a API retornará um status `200 OK` com o seguinte corpo:

```json
{
  "api_status": "ok",
  "data_connectivity": "ok"
}
```

**Cenário de Falha (Fonte de Dados Inacessível):**

Se o arquivo `books.csv` **não** for encontrado (por exemplo, o scraper ainda não foi executado), a API retornará um status `503 Service Unavailable` com o corpo:

```json
{
  "api_status": "ok",
  "data_connectivity": "not connected"
}
```

### Documentação Interativa da API

O FastAPI gera automaticamente uma documentação interativa. Com o servidor rodando, acesse as seguintes URLs no seu navegador para explorar e testar todos os endpoints:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

## Sistema de Web Scraping

O projeto inclui um script de web scraping robusto e automatizado, desenvolvido em Python, com o objetivo de extrair dados do site de e-commerce de livros [https://books.toscrape.com/](https://books.toscrape.com/).

O scraper foi construído para navegar por todas as páginas do site. Os dados extraídos incluem: 

* Título
* Preço
* Rating (classificação por estrelas) 
* Disponibilidade
* Categoria
* URL da imagem da capa

### Como Executar o Scraper

Para executar o script e popular a base de dados, siga os passos abaixo a partir do diretório raiz do projeto:

1.  **Ative seu ambiente virtual:**
    ```bash
    source venv/bin/activate
    # No Windows, o comando é: venv\Scripts\activate
    ```

2.  **Instale as dependências (caso ainda não tenha feito):**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute o script de scraping:**
    ```bash
    python scripts/scraper.py
    ```

### O que esperar após a execução

Ao rodar o script, você verá os **logs do processo sendo exibidos em tempo real no seu terminal**. As mensagens informarão o progresso, como a página atual que está sendo raspada e o resumo final.

Além disso, o script produzirá o seguinte resultado:

* **Arquivo de Dados:** Será criada uma pasta `data/` na raiz do projeto e dentro dela o arquivo `books.csv`. Este arquivo conterá todos os dados dos livros extraídos e será sobrescrito a cada nova execução para garantir que os dados estejam sempre atualizados.
