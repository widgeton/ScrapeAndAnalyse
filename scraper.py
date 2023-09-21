import requests
from bs4 import BeautifulSoup
import customtkinter as ctk

LINK = 'https://www.labirint.ru'


def scrape_books(bar: ctk.CTkProgressBar) -> list[list[str]]:
    pages = 10
    step = 1 / pages
    progress = step
    result = []
    session = requests.Session()
    bar.start()
    for i in range(1, pages + 1):
        url = LINK + f'/rating/?period=2&id_genre=1852&onpage=100&page={i}'
        respond = session.get(url)
        soup = BeautifulSoup(respond.text, 'lxml')
        books = soup.findAll('div', class_='product-padding')
        for book in books:
            title = book.find('span', class_='product-title').text.strip()

            author = book.find('div', class_='product-author')
            author = 'Без автора' if author is None else author.text.strip()

            pub_house = book.find('a', class_='product-pubhouse__pubhouse')
            pub_house = 'Без издательства' if pub_house is None else pub_house.text.strip()

            price = book.find('span', class_='price-val').text.strip()
            price = price.strip(' ₽').replace(' ', '')
            if not price.isdecimal():
                continue

            link = book.find('a', class_='cover').get('href')
            result.append([title, author, pub_house, price, link])
        bar.set(progress := progress + step)
        bar.master.update()
    bar.set(1)
    bar.stop()
    return result
