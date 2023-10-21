
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
import re

def extract_url(url):
    try:
        if not url.endswith('/'):
            url += '/'  # Add a trailing slash if it's missing

        response = requests.get(url)
        response.raise_for_status()  # Check for status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        print(f"{Fore.GREEN}\n[+] The links: [+]\n{Style.RESET_ALL}")

        for link in soup.find_all('a'):
            href = link.get('href')
            if re.match(r'(https?|ftp)://\S+|www\.\S+|\w+\.\w+', href):
                links.add(href)
            elif href.startswith('/'):
                links.add(url + href[1:])  # Remove the leading slash and add to the URL
            else:
                links.add(url + href)

        for link in links:
            print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_url = input("The url: ")
    extract_url(input_url)

