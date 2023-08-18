import nmap
import sys
import re
import requests
from requests.exceptions import ConnectTimeout, ConnectionError
import threading
import os

os.system("rm -r results")

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py -l <input_file>")
        return

    scanner = nmap.PortScanner()
    input_file = None
    nmap_arguments = "-sV"  # Added -sV for service version detection
    os.system("mkdir results")

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-l":
            input_file = sys.argv[i + 1]
            break

    if input_file is None:
        print("Usage: python script.py -l <input_file>")
        return

    with open(input_file, "r") as f:
        host_list = f.read().splitlines()

    threads = []

    for host in host_list:
        thread = threading.Thread(target=scan_host, args=(scanner, host, nmap_arguments))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def scan_host(scanner, host, arguments):
    try:
        scan_dict = scanner.scan(host, arguments=arguments)
        process_ports(scan_dict, host)
    except nmap.PortScannerError as e:
        print(f"Error scanning host {host}: {e}")

def process_ports(scan_dict, host):
    with open("./results/nmap_info.txt", "a") as g, \
         open("./results/nmap_detailed_info.txt", "a") as h, \
         open("./results/domain.txt", "a") as e, \
         open("./results/ip.txt", "a") as k:

        g.write(f"{host}:")
        h.write(f"{host}:\n")

        scaninfo = scan_dict['nmap']['scaninfo']
        protocol_list = list(scaninfo.keys())

        h.write(f" Protocols used: {protocol_list}\n")

        if "udp" in protocol_list:
            udp_dict = scan_dict['scan'][host]['udp']
            process_ports_helper(udp_dict, host, g, h, k, e)

        if "tcp" in protocol_list:
            tcp_dict = scan_dict['scan'][host]['tcp']
            process_ports_helper(tcp_dict, host, g, h, k, e)

        g.write("\n")
        h.write("\n")

def process_ports_helper(port_dict, host, g, h, k, e):
    for port, value in port_dict.items():
        g.write(f"{port},")
        k.write(f"{port},")
        h.write(f" ### Port {port}: {value['name']} {value['version']}\n")

    try:
        check_and_write_url(host, g, h, e)
    except (ConnectTimeout, ConnectionError) as ex:
        print(f"Error processing URL for {host}: {ex}")

def check_and_write_url(host, g, h, e):
    protocols = ["http://", "https://"]
    url = None

    for protocol in protocols:
        try:
            requests.get(f"{protocol}{host}", timeout=1)
            url = f"{protocol}{host}"
            break
        except (ConnectTimeout, ConnectionError):
            pass

    if url:
        g.write(f" {url}\n")
        h.write(f" {url}\n")
        e.write(f" {url}\n")
        print("URL:", url)
    else:
        print("No valid URL found for:", host)

def is_ip(text):
    ip_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return bool(ip_pattern.match(text))

if __name__ == "__main__":
    main()

