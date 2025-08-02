import requests
from bs4 import BeautifulSoup
import csv
import os
import logging

# Configuração do Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Variaveis de configuração
BASE_URL = 'https://books.toscrape.com/'
START_URL = f'{BASE_URL}catalogue/page-1.html'
OUTPUT_CSV_PATH = os.path.join('data', 'books.csv')

def get_soup(url):
    """Faz uma requisição GET para a URL e retorna um objeto BeautifulSoup."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a URL {url}: {e}")
        return None

def scrape_book_details(book_url):
    """Raspa os detalhes de um único livro a partir de sua página de detalhes."""
    soup = get_soup(book_url)
    if not soup:
        logging.warning(f"Não foi possível obter detalhes do livro em: {book_url}")
        return None

    try:
        title = soup.find('h1').text
        
        raw_price = soup.find('p', class_='price_color').text
        price = raw_price.replace('£', '')
        
        rating_tag = soup.find('p', class_='star-rating')
        rating = rating_tag['class'][1] if rating_tag else 'N/A' # Ex: 'Three'
        
        availability_tag = soup.find('p', class_='instock availability')
        availability = availability_tag.text.strip() if availability_tag else 'N/A'
        
        image_tag = soup.find('div', class_='item active').find('img')
        image_url = BASE_URL + image_tag['src'].replace('../', '') if image_tag else 'N/A'
        
        category_tag = soup.find('ul', class_='breadcrumb').find_all('li')[2].find('a')
        category = category_tag.text if category_tag else 'N/A'
        
        return {
            'title': title,
            'price': price,
            'rating': rating,
            'availability': availability,
            'category': category,
            'image_url': image_url
        }
    except AttributeError as e:
        logging.error(f"Erro ao extrair um atributo em {book_url}. O layout da página pode ter mudado. Erro: {e}")
        return None


def main():
    """Função principal para orquestrar o processo de web scraping."""
    logging.info("Iniciando o processo de web scraping...")
    
    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)
    
    headers = ['title', 'price', 'rating', 'availability', 'category', 'image_url']
    books_scraped_count = 0
    
    with open(OUTPUT_CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        
        current_url = START_URL
        page_num = 1
        
        # Loop para navegar por todas as páginas (paginação)
        while current_url:
            logging.info(f"Raspando página {page_num}: {current_url}")
            main_page_soup = get_soup(current_url)
            
            if not main_page_soup:
                logging.warning(f"Não foi possível processar a página {page_num}. Interrompendo.")
                break

            book_links = [
                BASE_URL + 'catalogue/' + a['href'].replace('../', '') 
                for a in main_page_soup.select('h3 > a')
            ]
            
            logging.info(f"Encontrados {len(book_links)} livros na página {page_num}.")
            
            for link in book_links:
                book_details = scrape_book_details(link)
                if book_details:
                    writer.writerow(book_details)
                    books_scraped_count += 1
            
            next_page_tag = main_page_soup.find('li', class_='next')
            if next_page_tag and next_page_tag.find('a'):
                next_page_href = next_page_tag.find('a')['href']
                current_url = BASE_URL + 'catalogue/' + next_page_href
                page_num += 1
            else:
                logging.info("Nenhuma outra página encontrada. Finalizando a navegação.")
                current_url = None
    
    # Logging de conclusão
    logging.info("=" * 50)
    logging.info("PROCESSO DE WEB SCRAPING CONCLUÍDO")
    logging.info(f"Total de livros coletados: {books_scraped_count}")
    logging.info(f"Dados salvos em: '{OUTPUT_CSV_PATH}'")
    logging.info("=" * 50)


if __name__ == '__main__':
    main()