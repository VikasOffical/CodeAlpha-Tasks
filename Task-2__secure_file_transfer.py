import socket
import os
from cryptography.fernet import Fernet

# Generate encryption key
key = b'aXx3m3PiizdLaptxzZsemq5qRNCjvNhLNdv4uInJY54='
cipher = Fernet(key)

# Server Code
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5050))  # Server IP & PORT
    server_socket.listen(1)
    print("[+] Server is Listening on 127.0.0.1:5050")

    conn, addr = server_socket.accept()
    print(f"[+] Connection established with {addr}")

    file_name = conn.recv(1024).decode()
    encrypted_data = conn.recv(4096)

    # Decrypt the data
    data = cipher.decrypt(encrypted_data)

    with open(f"received_{file_name}", 'wb') as f:
        f.write(data)

    print(f"[+] File received and saved as received_{file_name}")

    conn.close()
    server_socket.close()


# Client Code
def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Correct way to connect to server
    client_socket.connect(('127.0.0.1',5050))

    file_name = input("Enter file name to send: ")

    if not os.path.exists(file_name):
        print("[-] File not found!")
        return

    with open(file_name, 'rb') as f:
        data = f.read()

    encrypted_data = cipher.encrypt(data)

    client_socket.send(file_name.encode())
    client_socket.send(encrypted_data)

    print("[+] File sent successfully!")

    client_socket.close()


# Main Program
choice = input("Server or Client? (s/c): ")

if choice.lower() == 's':
    server()
elif choice.lower() == 'c':
      client()
else:
    print("[-] Invalid Choice!")
