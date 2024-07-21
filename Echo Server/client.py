import socket
import time

HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP, PORT))

    while True:

        full_message = ""

        while True:

            header = s.recv(HEADERSIZE)

            if not header:

                break

            message_length = int(header.decode('utf-8'))

            while message_length - len(full_message) > 0:

                message = s.recv(HEADERSIZE)

                full_message += message.decode('utf-8')
            
            print(f"{full_message}\n")

            break 
        
        # send a response

        response = "Hello, World! This is a really really really long message!"

        response_header = f"{len(response):<{HEADERSIZE}}"

        response = response_header + response

        s.send(response.encode('utf-8'))

        time.sleep(1)