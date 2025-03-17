TCP Client-Server Design Explanation

Overview:
This document explains the design and functionality of the TCP client-server project. The server handles multiple client connections using multi-threading, while the client allows secure communication using AES encryption.

Architecture:

The server listens on a specific port for incoming client connections.
When a client connects, the server spawns a new thread to handle communication with that client.
The client sends encrypted messages to the server, which decrypts them and logs them.
The server responds with an acknowledgment, encrypted and sent back to the client.
The client can send multiple messages until it chooses to exit.

Threading Model:

The server uses multi-threading to handle multiple clients concurrently.
Each client connection runs in a separate thread to ensure simultaneous communication.
A while-loop ensures continuous message handling without closing the connection after a single message.

Encryption Implementation:
The project uses AES-128-CBC encryption to secure message transmission.
A predefined 16-byte key and IV are used for encryption and decryption.
Messages are padded using PKCS7 before encryption and base64 encoded before transmission.
The server decrypts received messages, processes them, and sends back an encrypted acknowledgment.

Conclusion:
This design ensures secure, multi-threaded communication between clients and the server.
