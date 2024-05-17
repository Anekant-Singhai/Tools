import struct
import socket

class IcmpPacketSender:
    def __init__(self, target_ip, port=None, ttl=64, icmp_id=12321, data=None):
        self.target_ip = target_ip
        self.port = port
        self.data = data
        self.ttl = ttl
        self.icmp_id = icmp_id

    def send_icmp_packet(self):
        icmp_type = 8
        icmp_code = 0
        icmp_checksum = 0
        icmp_sequence = 1

        if self.data:
            icmp_payload = self.data.encode()
        else:
            icmp_payload = b"Hidden MSG Lmao!"

        icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, self.icmp_id, icmp_sequence)
        icmp_checksum = self.calculate_checksum(icmp_header + icmp_payload)
        icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, socket.htons(icmp_checksum), self.icmp_id, icmp_sequence)
        icmp_packet = icmp_header + icmp_payload

        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack("I", self.ttl))
            sock.settimeout(3)
            if self.port:
                sock.sendto(icmp_packet, (self.target_ip, self.port))
            else:
                sock.sendto(icmp_packet, (self.target_ip, 0))
            print("ICMP packet sent successfully!")

    def calculate_checksum(self, data):
        checksum = 0

        if len(data) % 2 != 0:
            data += b"\x00"

        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i + 1]

        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += checksum >> 16

        return (~checksum) & 0xffff

def main():
    target_ip = input("Enter target IP: ")
    port = input("Enter port (optional, press Enter to skip): ")
    port = int(port) if port else None
    data = input("Enter data/command (optional, press Enter to use default): ")
    ttl = input("Enter TTL (optional, press Enter to use default): ")
    ttl = int(ttl) if ttl else 64
    icmp_id = input("Enter ICMP ID (optional, press Enter to use default): ")
    icmp_id = int(icmp_id) if icmp_id else 12321

    icmp_packet_sender = IcmpPacketSender(target_ip, port, ttl, icmp_id, data)
    icmp_packet_sender.send_icmp_packet()

if __name__ == "__main__":
    main()
