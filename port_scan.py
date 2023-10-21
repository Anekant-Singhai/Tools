import socket
import threading
from queue import Queue

target = input("target: ")
queue = Queue()
open_ports = []

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((target,port))
        return True
    except:
        return False

def get_ports(mode):
    if mode == 1:
        for port in range(1,1024):
            queue.put(port)
    elif mode == 2:
        for port in range(1,10000):
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 139, 443 , 445 , 1337 , 3306]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        ports = input("The ports you need seperated by space: ")
        ports = ports.split()
        ports = list(map(int,ports))
        for port in ports:
            queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"[+] Port {port} is open")
            open_ports.append(port)


def runscanner(threads , mode):
    get_ports(mode)
    thread_list = []
    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    print("open ports: ",open_ports)  




runscanner(100, int(input("The modes: 1 for 1000 , 2 for 10000 , 3 top ports ,4 custom: ")))



