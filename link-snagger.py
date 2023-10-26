import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from urllib.parse import urljoin, urlparse
import argparse
import sys

def extract_url(url, output_file, js_only, links_only):
    # The code for extracting URLs goes here, using the provided arguments.
    try:
        if not url.endswith('/'):
            url += '/'  # Add a trailing slash if it's missing
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # Check for status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        links_js = set()

        if not js_only and not links_only:
            print(f"{Fore.GREEN}\n[+] The links: [+]\n{Style.RESET_ALL}")

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)
                if parsed_url.scheme and parsed_url.netloc:
                    links.add(absolute_url)

        if not links_only:
            for script in soup.find_all('script', src=True):
                src = script.get('src')
                if src:
                    absolute_url = urljoin(url, src)
                    parsed_url = urlparse(absolute_url)
                    if parsed_url.scheme and parsed_url.netloc:
                        links_js.add(absolute_url)

        if not output_file:
            output_stream = sys.stdout
        else:
            output_stream = open(output_file, 'w')
            if links:
                for link in links:
                    output_stream.write(link+"\n")
            if links_js:
                for link in links_js:
                    output_stream.write(link+"\n")
            output_stream.close()
        for link in links:
            print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")
        print(f"\n")
        if not js_only:
            print(f"---------------------- THE JS links: -------------------")
            for link in links_js:
                print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract URLs from a web page.")
    parser.add_argument("-u", "--url", help="URL to extract links from", required=False)
    parser.add_argument("-o", "--output", help="Output file to save the links", required=False)
    parser.add_argument("-js", "--js-only", action="store_true", help="Only extract JavaScript links", required=False)
    parser.add_argument("-l", "--links-only", action="store_true", help="Only extract links, no JS files", required=False)
    
    args = parser.parse_args()
    
    if args.url:
        input_url = args.url
        extract_url(input_url, args.output, args.js_only, args.links_only)
    else:
        print("Please provide a URL. Use -h or --help for usage information.")


