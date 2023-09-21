import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd

# Configuration
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

# Vérifie le numéro de la page actuelle


def checkCurrentPage(soup):
    current = soup.find('li', class_="current").text.strip()
    match = re.match(r"Page (\d+) of 50", current)
    if match:
        current_page = int(match.group(1))
    return current_page

# Recupère les données de la page actuelle


def get_book_data(soup):
    book = {}
    books = []
    if soup:
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
            title = title_element.get('title')
            price = price_element.text.strip()
            book = {
                "titre": title,
                "prix": price,
            }
            books.append(book)
        return books


def navigateInPage(driver, soup):
    all_book = []
    current_page = checkCurrentPage(soup)
    while current_page < 50:
        books = get_book_data(soup)
        all_book.append(books)
        next_link = driver.find_element(By.XPATH, "//a[text()='next']")
        next_link.click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        current_page = checkCurrentPage(soup)
    return all_book


driver.get("https://books.toscrape.com/")
soup = BeautifulSoup(driver.page_source, "html.parser")
result = navigateInPage(driver, soup)
# compréhension de liste pour aplatir la structure
liste_aplatie = [item for sublist in result for item in sublist]
df = pd.DataFrame(liste_aplatie)
df.to_csv('donnees.csv', index=False)
# print(df)


# def request():
#     try:
#         response = requests.get(URL)
#         if response.status_code == 200:
#             print('done')
#         else:
#             print(
#                 f"La requête a échoué avec le code de statut : {response.status_code}")
#     except Exception as e:
#         print(f'une erreur {e} ')
#     return response
