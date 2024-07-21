import socket
import time

HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, PORT))
    s.listen()

    conn, addr = s.accept()
    print(f"Connection from {addr[0]}:{addr[1]} accepted!\n")

    with conn:

        welcome = "Welcome to the server!"

        welcome_header = f"{len(welcome):<{HEADERSIZE}}"

        welcome = (welcome_header + welcome).encode('utf-8')

        conn.send(welcome)

        while True:

            full_message = ""

            while True:
                
                header = conn.recv(HEADERSIZE)

                if not header:

                    break

                message_length = int(header.decode('utf-8'))

                while message_length - len(full_message) > 0:

                    message = conn.recv(HEADERSIZE)

                    full_message += message.decode('utf-8')

                break

            print(f"{full_message}\n")

            new_message_header = f"{len(full_message):<{HEADERSIZE}}"

            response = new_message_header + full_message

            conn.send(response.encode('utf-8'))

            time.sleep(1)