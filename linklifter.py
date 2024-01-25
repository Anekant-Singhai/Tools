# import requests
# from bs4 import BeautifulSoup
# from colorama import Fore, Style
# from urllib.parse import urljoin, urlparse
# import argparse
# import sys

# class linklifter:
#     def extract_url(self,url, output_file, js_only, links_only):
#         # The code for extracting URLs goes here, using the provided arguments.
#         try:
#             if not url.endswith('/'):
#                 url += '/'  # Add a trailing slash if it's missing
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
#             }
#             response = requests.get(url, headers=headers,verify=False)
#             response.raise_for_status()  # Check for status codes
#             soup = BeautifulSoup(response.text, 'html.parser')
#             links = set()
#             links_js = set()

#             if not js_only and not links_only:
#                 print(f"{Fore.GREEN}\n[+] The links: [+]\n{Style.RESET_ALL}")

#             for link in soup.find_all('a'):
#                 href = link.get('href')
#                 if href:
#                     absolute_url = urljoin(url, href)
#                     parsed_url = urlparse(absolute_url)
#                     if parsed_url.scheme and parsed_url.netloc:
#                         links.add(absolute_url)
                        

#             if not links_only:
#                 for script in soup.find_all('script', src=True):
#                     src = script.get('src')
#                     if src:
#                         absolute_url = urljoin(url, src)
#                         parsed_url = urlparse(absolute_url)
#                         if parsed_url.scheme and parsed_url.netloc:
#                             links_js.add(absolute_url)

#             if not output_file:
#                 output_stream = sys.stdout
#             else:
#                 output_stream = open(output_file, 'w')
#                 if links:
#                     for link in links:
#                         output_stream.write(link+"\n")
#                 if links_js:
#                     for link in links_js:
#                         output_stream.write(link+"\n")
#                 output_stream.close()
#             for link in links:
#                 print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")
#             print(f"\n")
#             if not js_only:
#                 print(f"---------------------- THE JS links: -------------------")
#                 for link in links_js:
#                     print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")

#         except requests.exceptions.RequestException as e:
#             print(f"Error: {e}")
#         pass

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Extract URLs from a web page.")
#     parser.add_argument("-u", "--url", help="URL to extract links from", required=False)
#     parser.add_argument("-o", "--output", help="Output file to save the links", required=False)
#     parser.add_argument("-js", "--js-only", action="store_true", help="Only extract JavaScript links", required=False)
#     parser.add_argument("-l", "--links-only", action="store_true", help="Only extract links, no JS files", required=False)
    
#     args = parser.parse_args()
#     linkfter = linklifter()
#     if args.url:
#         input_url = args.url
#         linkfter.extract_url(input_url, args.output, args.js_only, args.links_only)
#     else:
#         print("Please provide a URL. Use -h or --help for usage information.")
#     pass


# '''
# In the __init__.py file:

# from .linklifter import LinkLifter

# linklifter/
# ├── __init__.py
# └── linklifter.py


# setup.py file:

# from setuptools import setup

# setup(
#     name='linklifter',
#     version='1.0',
#     packages=['linklifter'],
#     install_requires=[
#         'requests',
#         'beautifulsoup4',
#         'colorama',
#     ],
# )

# python setup.py sdist

# from linklifter import LinkLifter

# linklifter = LinkLifter()
# linklifter.extract_url("https://example.com", "output.txt", js_only=True, links_only=False)

# '''



import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from urllib.parse import urljoin, urlparse
import argparse
import sys

class linklifter:
    def extract_url(self,url, output_file, js_only, links_only):
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
            links_css = set() # for css links


            if not js_only and not links_only:
                print(f"{Fore.GREEN}\n[+] The links: [+]\n{Style.RESET_ALL}")
            
            if not js_only:
                for css_link in soup.find_all('link', rel='stylesheet', href=True):
                    href = css_link.get('href')
                    if href:
                        absolute_url = urljoin(url, href)
                        parsed_url = urlparse(absolute_url)
                        if parsed_url.scheme and parsed_url.netloc:
                            links_css.add(absolute_url)


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
                if links_css:
                    for link in links_css:
                        output_stream.write(link + "\n")
                output_stream.close()
            for link in links:
                print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")
            print(f"\n")
            if not js_only:
                print(f"---------------------- THE JS links: -------------------")
                for link in links_js:
                    print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")
            # Before closing the output_stream

            # Printing the links
            print(f"---------------------- THE CSS links: -------------------")
            for link in links_css:
                print(f"{Fore.LIGHTMAGENTA_EX} 🢂 {link}{Style.RESET_ALL}\n")


        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract URLs from a web page.")
    parser.add_argument("-u", "--url", help="URL to extract links from", required=False)
    parser.add_argument("-o", "--output", help="Output file to save the links", required=False)
    parser.add_argument("-js", "--js-only", action="store_true", help="Only extract JavaScript links", required=False)
    parser.add_argument("-l", "--links-only", action="store_true", help="Only extract links, no JS files", required=False)
    
    args = parser.parse_args()
    linkfter = linklifter()
    if args.url:
        input_url = args.url
        linkfter.extract_url(input_url, args.output, args.js_only, args.links_only)
    else:
        print("Please provide a URL. Use -h or --help for usage information.")
    pass


'''
In the __init__.py file:

from .linklifter import LinkLifter

linklifter/
├── __init__.py
└── linklifter.py


setup.py file:

from setuptools import setup

setup(
    name='linklifter',
    version='1.0',
    packages=['linklifter'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'colorama',
    ],
)

python setup.py sdist

from linklifter import LinkLifter

linklifter = LinkLifter()
linklifter.extract_url("https://example.com", "output.txt", js_only=True, links_only=False)

'''





