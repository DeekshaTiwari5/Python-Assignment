import requests
from bs4 import BeautifulSoup
from database import engine, Book
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

base_url = 'http://books.toscrape.com/catalogue/page-{}.html'

for page_num in range(1, 51):
    url = base_url.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        
        # Fix encoding issue for price
        price_str = book.find('p', class_='price_color').text.strip('£')
        price = float(price_str.replace('Â', '').replace('£', '').strip())

        availability = 'In stock' in book.find('p', class_='instock availability').text
        rating_text = book.find('p', class_='star-rating')['class'][1]
        # Convert rating text to integer
        ratings = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        rating = ratings.get(rating_text)

        new_book = Book(title=title, price=price, availability=availability, rating=rating)
        session.add(new_book)
        session.commit()
