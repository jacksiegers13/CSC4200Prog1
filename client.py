#CSC4200-Client
#Jack Siegers
#3/16/2025

import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Encryption settings
KEY = b'ThisIsASecretKey'  # 16 bytes for AES-128
IV = b'ThisIsAnIVVector'  # 16 bytes IV

#Encryption messages
def encrypt_message(message):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(encrypted_bytes).decode()

def decrypt_message(encrypted_message):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_bytes = unpad(cipher.decrypt(base64.b64decode(encrypted_message)), AES.block_size)
    return decrypted_bytes.decode()

# TCP Client
class TCPClient:
    def __init__(self, server_host='127.0.0.1', server_port=12345):
        self.server_host = server_host
        self.server_port = server_port
    
    def send_message(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_host, self.server_port))
        
        while True:
            encrypted_message = encrypt_message(message)
            client_socket.send(encrypted_message.encode())
            response = decrypt_message(client_socket.recv(1024).decode())
            print(f"Server response: {response}")

            # Ask for more messages
            message = input("Enter a message (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                break

        client_socket.close()

if __name__ == "__main__":
    client = TCPClient()
    first_message = input("Enter a message: ")
    client.send_message(first_message)
