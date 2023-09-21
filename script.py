import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"


def request():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print('done')
        else:
            print(
                f"La requête a échoué avec le code de statut : {response.status_code}")
    except Exception as e:
        print(f'une erreur {e} ')
    return response


def get_book_data():
    book = {}
    books = []
    response = request()
    if response:
        page = response
        soup = BeautifulSoup(page.content, "html.parser")
        firstSection = soup.find('section')
        divs = firstSection.find_all('div')
        second_div = divs[1]
        ol = second_div.find('ol')
        lis = ol.find_all('li')
        for li in lis:
            article = li.find('article')
            title_element = (article.find('h3')).find('a')
            price_element = (article.find("div", class_="product_price")).find(
                "p", class_="price_color")
            title = title_element.text.strip()
            price = price_element.text.strip()
            book = {
                "titre": title,
                "prix": price,
            }
            books.append(book)
        return books


books = get_book_data()
print(books)
