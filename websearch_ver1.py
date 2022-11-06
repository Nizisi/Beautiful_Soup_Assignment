from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import sys
import re

if __name__ == '__main__':
    
    for keyword in sys.argv[1:]:
        keyword = keyword.capitalize()
        url = f'https://en.wikipedia.org/wiki/{keyword}_(disambiguation)'

        try:
            response = requests.get(url)
            response.raise_for_status()


        except HTTPError as httperr:
            print(f'HTTP ERROR: {httperr}')
            sys.exit(1)

        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href = re.compile(keyword)):
            title = link.get('title')
            print(f'{title} : ',link['href'])