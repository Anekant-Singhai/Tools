import socket
import threading
from queue import Queue
import errno
from colorama import Fore, Style


target = input("Target: ")
queue = Queue()
open_ports = []

def scan_port(protocol, port):
    try:
        sock = socket.socket(socket.AF_INET, protocol)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            return True
        return False
    except Exception as e:
        return False

def get_ports(protocol, mode):
    if protocol == socket.SOCK_STREAM:
        if mode == 1:
            for port in range(1, 1025):
                queue.put(port)
        elif mode == 2:
            for port in range(1, 10001):
                queue.put(port)
        elif mode == 3:
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1337, 3306, 8080]
            for port in ports:
                queue.put(port)
        elif mode == 4:
            custom_ports = input("Enter custom ports separated by space: ")
            ports = list(map(int, custom_ports.split()))
            for port in ports:
                queue.put(port)
    if protocol == socket.SOCK_DGRAM:
        if mode == 1:
            for port in range(1, 1025):
                queue.put(port)
        elif mode == 2:
            for port in range(1, 10001):
                queue.put(port)
        elif mode == 3:
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1337, 3306, 8080]
            for port in ports:
                queue.put(port)
        elif mode == 4:
            custom_ports = input("Enter custom ports separated by space: ")
            ports = list(map(int, custom_ports.split()))
            for port in ports:
                queue.put(port)

def worker(protocol):
    while not queue.empty():
        port = queue.get()
        if scan_port(protocol, port):
            print(f"[+] Port {Fore.GREEN} {port} {Style.RESET_ALL} is open")
            open_ports.append(port)

def banner_ip(banners, address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((address, port))
        if port == 80:
            print("\n" + Fore.GREEN + "[+] HTTP PROTOCOL Found" + Style.RESET_ALL + f" - IP: {address} | PORT: {port}")
            message = b"GET / HTTP/1.1\r\n\r\n"
            s.sendall(message)
        banner_data = s.recv(4096)
        banners.append([(address, port), banner_data.decode('utf-8')])
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED:
            pass
        else:
            print(Fore.RED + f"[-] Error connecting to IP: {address} | PORT: {port}" + Style.RESET_ALL)
    s.close()

def run_scanner(threads, mode, protocol):
    get_ports(protocol, mode)
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=worker, args=(protocol,))
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("\nOpen ports:", open_ports)

print("Select a protocol:")
print("1. TCP")
print("2. UDP")
protocol_choice = int(input("Enter the protocol number (1 or 2): "))

if protocol_choice == 1:
    run_scanner(200, int(input("Select a mode: 1 for 1024, 2 for 10000, 3 for common ports, 4 for custom: ")), socket.SOCK_STREAM)
elif protocol_choice == 2:
    run_scanner(200, int(input("Select a mode: 1 for 1024, 2 for 10000, 3 for common ports, 4 for custom: ")), socket.SOCK_DGRAM)
else:
    print("Invalid protocol choice. Please select 1 or 2 for TCP or UDP.")

# print("\n[+] Attempting banner grabbing now: [+]")
# banners = []
# for port in open_ports:
#     banner_ip(banners, target, port)

# for banner in banners:
#     print("IP:", banner[0][0], "Port:", banner[0][1])
#     print("Banner:", banner[1])
print(" [+] Attempting the banner grabbing now: [+]")
banners = []
for port in open_ports:
    banner_ip(banners, target, port)
for banner in banners:
    print(Fore.CYAN + f"BANNER for IP: {banner[0][0]} | PORT: {banner[0][1]}" + Style.RESET_ALL)
    print(f"🏁  ->  \n {banner[1]}")
    print(f"         -------------------------------------------------------------------------------------------      \n")

