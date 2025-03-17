#CSC4200-Server
#Jack Siegers
#3/16/2025

import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Encryption settings
KEY = b'ThisIsASecretKey'  # 16 bytes for AES-128
IV = b'ThisIsAnIVVector'  # 16 bytes IV

def encrypt_message(message):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(encrypted_bytes).decode()

def decrypt_message(encrypted_message):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_bytes = unpad(cipher.decrypt(base64.b64decode(encrypted_message)), AES.block_size)
    return decrypted_bytes.decode()

# TCP Server
class TCPServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
    
    def handle_client(self, client_socket, addr):
        print(f"New connection from {addr}")
        try:
            while True:
                encrypted_message = client_socket.recv(1024).decode()
                if not encrypted_message:
                    break
                message = decrypt_message(encrypted_message)
                print(f"Received from {addr}: {message}")
                
                response = encrypt_message("Acknowledged")
                client_socket.send(response.encode())
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            print(f"Closing connection from {addr}")
            client_socket.close()
    
    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True)
            client_thread.start()
