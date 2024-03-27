import requests
from bs4 import BeautifulSoup
import json

# Function to scrape quotes and authors from a single page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract quotes and authors from the page
    quotes = []
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes.append({'quote': text, 'author': author, 'tags': tags})

    # Extract author information
    authors = []
    for author in soup.find_all('div', class_='author-details'):
        fullname = author.find('h3').text.strip()
        born_info = author.find('span', class_='author-born-date').text.strip()
        location = author.find('span', class_='author-born-location').text.strip()[3:]  # remove 'in ' prefix
        description = author.find_next_sibling('div', class_='author-description').text.strip()
        authors.append({'fullname': fullname, 'born_date': born_info, 'born_location': location, 'description': description})

    return quotes, authors

# Function to scrape quotes from all pages
def scrape_quotes():
    quotes = []
    authors = []
    page = 1
    while True:
        url = f'http://quotes.toscrape.com/page/{page}/'
        page_quotes, page_authors = scrape_page(url)
        if not page_quotes:
            break  # No more quotes found, end loop
        quotes.extend(page_quotes)
        authors.extend(page_authors)
        page += 1
    return quotes, authors

# Main function
def main():
    # Scrape quotes and authors
    quotes, authors = scrape_quotes()

    # Save quotes to quotes.json
    with open('quotes.json', 'w') as quotes_file:
        json.dump(quotes, quotes_file, indent=2)

    # Save authors to authors.json
    with open('authors.json', 'w') as authors_file:
        json.dump(authors, authors_file, indent=2)

if __name__ == "__main__":
    main()