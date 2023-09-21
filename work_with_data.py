from datetime import date
from scraper import scrape_books
import os
import pandas as pn


def write(bar):
    books_list = scrape_books(bar)
    df = pn.DataFrame(books_list, columns=['title', 'author', 'pub_house', 'price', 'link'])
    df.to_csv(f'./data/{date.today()}.csv', sep=';')


def get_top_pub_houses_by_book_amount(date: str, top: int):
    df = pn.read_csv(f'data/{date}.csv', sep=';')
    pub_houses = df.groupby('pub_house')['title'].count().sort_values(ascending=False).head(top)
    return pub_houses.index


def books_amount(date: str, pub_houses: list[str]):
    df = pn.read_csv(f'./data/{date}.csv', sep=';')

    lst = df.groupby('pub_house')['title'].count().reset_index()
    top = lst.query('pub_house in @pub_houses').sort_values(by='title', ascending=False)
    others = lst.query('pub_house not in @pub_houses')['title'].sum()
    others = pn.DataFrame([['Другие', others]], columns=top.columns)
    result = pn.concat([top, others])

    return result.iloc[::-1]


def middle_price(date: str, pub_houses: list[str]):
    df = pn.read_csv(f'data/{date}.csv', sep=';')

    pub_house = df.groupby('pub_house')['price'].mean().reset_index()
    pub_house = pub_house.query('pub_house in @pub_houses').sort_values(by='price')
    return pub_house


def get_dates(amount):
    dates = [i.strip('.csv') for i in os.listdir('./data')]
    last = dates[-1]
    if len(dates) > amount:
        div = len(dates) // amount
        dates = [item for i, item in enumerate(dates) if not i % div]
    if last != dates[-1]:
        dates.append(last)
    return dates


def changes_of_books_amount(pub_houses: list[str]):
    dates = get_dates(20)
    lst = []
    for i in dates:
        books = books_amount(i, pub_houses)
        books['date'] = pn.Series([i] * len(books['title']), index=books.index)
        lst.append(books)

    result = pn.concat(lst).pivot(index='pub_house', values='title', columns='date')
    result = result.drop(labels='Другие')
    result = result.fillna(value=0)
    return result


def changes_of_middle_prices(pub_houses: list[str]):
    dates = get_dates(20)
    lst = []
    for i in dates:
        books = middle_price(i, pub_houses)
        books['date'] = pn.Series([i] * len(books['price']), index=books.index)
        lst.append(books)

    result = pn.concat(lst).pivot(index='pub_house', values='price', columns='date')
    result = result.fillna(value=0)
    return result
