
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
import re

def extract_url(url):
    try:
        if not url.endswith('/'):
            url += '/'  # Add a trailing slash if it's missing
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
        response = requests.get(url,headers=headers,verify=False)
        response.raise_for_status()  # Check for status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        links_js = set()
        print(f"{Fore.GREEN}\n[+] The links: [+]\n{Style.RESET_ALL}")

        for link in soup.find_all('a'):
            href = link.get('href')
            if re.match(r'(https?|ftp)://\S+|www\.\S+|\w+\.\w+', href):
                links.add(href)
            elif href.startswith('/'):
                links.add(url + href[1:])  # Remove the leading slash and add to the URL
            else:
                links.add(url + href)
        # for js embedded links
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                if re.match(r'(https?|ftp)://\S+|www\.\S+|\w+\.\w+', src):
                    links_js.add(src)
                elif src.startswith('/'):
                    links_js.add(url + src)  # If the src starts with '/', add it to the base URL
                else:
                    links_js.add(src)

        for link in links:
            print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")
        print(f"\n")
        print(f"---------------------- THE JS links: -------------------")
        for link in links_js:
            print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_url = input("The url: ")
    extract_url(input_url)


