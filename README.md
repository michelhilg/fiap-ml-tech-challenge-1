# fiap-ml-tech-challenge-1

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
