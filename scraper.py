import requests
from bs4 import BeautifulSoup

def get_book_data(url: str) -> dict:
    """
    функция собирает данные об одной книге, размещенной на указанном сайте.
    данные включают название, рейтинг, цену, количество в наличии, описание и доп.характеристики
    для работы функции нужен адрес страницы
    функция возвращает словарь с указанными данными
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    response = requests.get(url)
    response.encoding = 'utf-8'
    response.raise_for_status()


    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find('h1').text.strip()

    price = soup.find(class_='price_color').text.strip()

    availability = soup.find(class_="availability").text.strip()

    rating_class = soup.find(class_='star-rating')['class']
    rating = next((r for r in rating_class if r != 'star-rating'), None)

    description = ''
    description_header = soup.find('h2', string='Product Description')
    if description_header:
        desc_p = description_header.find_next('p')
        if desc_p:
            description = desc_p.text.strip()

    info_table = soup.find('table', class_='table table-striped')
    product_info = {}
    if info_table:
        for row in info_table.find_all('tr'):
            key = row.find('th').text.strip()
            value = row.find('td').text.strip()
            product_info[key] = value

    book_data = {
        'title': title,
        'price': price,
        'availability': availability,
        'rating': rating,
        'description': description,
    }

    book_data.update(product_info)
    return book_data

    # КОНЕЦ ВАШЕГО РЕШЕНИЯ

import requests
from bs4 import BeautifulSoup

def scrape_books(is_save = False):
    """
    функция проходит по всем страницам сайта с каталогом
    осуществляет парсинг всех страниц ранее написанной функцией get_book_data
    
    """
    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    page_num = 1
    while True:
        url = base_url.format(page_num)
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("article.product_pod")
        if not books:
            break

        for book in books:
            book_url = "http://books.toscrape.com/catalogue/" + book.h3.a['href']
            data = get_book_data(book_url)
            all_books.append(data)
        page_num += 1

    if is_save:
        with open("books_data.txt", "w", encoding="utf-8") as f:
            for book in all_books:
                f.write(str(book) + "\n")

    return all_books
            
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ

import schedule
import time

# НАЧАЛО ВАШЕГО РЕШЕНИЯ
def reg_update():
    """
    функция регулярной сборки данных о книгах
    ежедневно в 19:00 запускается функция scrape_books
    заложен минутный интервал проверки не наступило ли время запуска функции
    """
    scrape_books(is_save=True)

schedule.every().day.at("19:00").do(reg_update)

while True:
    schedule.run_pending()
    time.sleep(60)
# КОНЕЦ ВАШЕГО РЕШЕНИЯ
