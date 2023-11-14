from rich.console import Console
import argparse
import json
import requests
import threading
from bs4 import BeautifulSoup
console = Console()

class RequestSender:
    def __init__(self, url, method='GET', headers=None, data=None, total_requests=None, output_file=None):
        self.url = url
        self.data = data
        self.method = method
        self.headers = headers
        self.total_requests = total_requests
        self.requests_sent = 0
        self.lock = threading.Lock()
        self.output_file = output_file

    def send_request(self):
        try:
            if self.total_requests is not None:
                with self.lock:
                    if self.requests_sent >= self.total_requests:
                        return False

            response = self.make_request()

            with self.lock:
                self.requests_sent += 1

            self.write_output(response)

        except Exception as e:
            console.log(f"[bold red]Error:[/bold red] {e}")

    def make_request(self):
        if self.method == 'GET':
            return requests.get(self.url, headers=self.headers)
        elif self.method == 'POST':
            return requests.post(self.url, headers=self.headers, data=self.data)
        elif self.method == 'PUT':
            return requests.put(self.url, headers=self.headers, data=self.data)
        elif self.method == 'DELETE':
            return requests.delete(self.url, headers=self.headers)
        elif self.method == 'OPTIONS':
            
            response =  requests.options(self.url, headers=self.headers)
            json_output = response.headers
            console.log("-> ",json_output['Allow'])
            return requests.options(self.url, headers=self.headers)
        elif self.method == 'HEAD':
            response = requests.get(self.url,headers=self.headers)
            console.log("The headers: ",response.headers)
            return requests.get(self.url,headers=self.headers)

        else:
            console.log(f"[bold red]Unsupported method:[/bold red] {self.method}")
            return None

    def write_output(self, response):
        if self.output_file:
            with open(self.output_file, 'a') as file:
                file.write("----------------RESPONSE----------------\n\n")
                if 'text/html' in response.headers.get('content-type', ''):
                    soup = BeautifulSoup(response.text, 'html.parser')
                    file.write(soup.prettify())
                else:
                    file.write(response.text + '\n')

        console.log(f"[blue]{self.method} request to {self.url} - Status code: {response.status_code}[/blue]")

def send_requests(url, method='GET', headers=None, data=None, num_threads=1, requests_per_second=1, total_requests=None, output_file=None):
    request_sender = RequestSender(url, method, headers, data, total_requests, output_file)
    delay = 1 / requests_per_second

    # Worker function for threads to run
    def send():
        while True:
            request_sender.send_request()
            if request_sender.send_request() == False:
                break

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join(delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Request Sender Tool")

    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-m", "--method", default="GET", help="HTTP method (GET, POST, PUT, DELETE, OPTIONS)")
    parser.add_argument("-H", "--headers", type=json.loads, default={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"}, help="Headers in JSON format")
    parser.add_argument("-d", "--data", type=json.loads, default={}, help="Data in JSON format for POST and PUT requests")
    parser.add_argument("-t","--num-threads", type=int, default=1, help="Number of threads")
    parser.add_argument("-rps","--requests-per-second", type=float, default=1, help="Requests per second")
    parser.add_argument("-tr","--total-requests", type=int, help="Total number of requests across all threads")
    parser.add_argument("-o", "--output-file", help="File to write the output to")

    args = parser.parse_args()

    send_requests(
        args.url,
        method=args.method,
        headers=args.headers,
        data=args.data,
        num_threads=args.num_threads,
        requests_per_second=args.requests_per_second,
        total_requests=args.total_requests,
        output_file=args.output_file
    )
