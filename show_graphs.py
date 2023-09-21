import work_with_data as wwd
import matplotlib.pyplot as plt


def show_books_amount(date: str, top: int):
    pub_houses = wwd.get_top_pub_houses_by_book_amount(date, top)
    books = wwd.books_amount(date, pub_houses)

    plt.rcParams.update({'figure.autolayout': True})

    fig, (ax, ax_pie) = plt.subplots(figsize=(14, 7), ncols=2, nrows=1)

    labels = books['pub_house']
    sizes = books['title']

    ax_pie.set_title('Распределение книг')
    explode = (0.15,) + (0,) * (len(books) - 1)
    ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, explode=explode, startangle=90)
    ax_pie.axis('equal')

    ax.barh(labels, sizes)
    ax.set(ylabel='Издатели', xlabel='Кол-во книг', title='Кол-во книг по издательствам')
    ax.grid(axis='x')

    plt.show()


def show_middle_price(date: str, top: int):
    pub_houses = wwd.get_top_pub_houses_by_book_amount(date, top)
    prices = wwd.middle_price(date, pub_houses)

    fig, ax = plt.subplots(figsize=(8, 6), layout='constrained')
    ax.barh(prices['pub_house'], prices['price'])
    ax.set(ylabel='Издатели', xlabel='Средняя цена книги', title='Цены книг по издательствам')
    ax.grid(axis='x')

    plt.show()


def show_changes_of_books_amount(date: str, top: int):
    pub_houses = wwd.get_top_pub_houses_by_book_amount(date, top)
    changes = wwd.changes_of_books_amount(pub_houses)

    fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
    for pub_house in changes.index:
        ax.plot(changes.columns, changes.query('pub_house == @pub_house').values[0], label=pub_house)

    ax.set(ylabel='Кол-во книг', xlabel='Дата', title='Кол-во книг издательства в топе по датам')
    ax.legend(loc='upper left')
    ax.grid()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    plt.show()


def show_changes_of_middle_prices(date: str, top: int):
    pub_houses = wwd.get_top_pub_houses_by_book_amount(date, top)
    changes = wwd.changes_of_middle_prices(pub_houses)

    fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
    for pub_house in changes.index:
        ax.plot(changes.columns, changes.query('pub_house == @pub_house').values[0], label=pub_house)

    ax.set(ylabel='Со. цена', xlabel='Дата', title='Ср. цена книг издательства в топе по датам')
    ax.legend(loc='upper left')
    ax.grid()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    plt.show()
