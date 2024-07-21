import socket 
import sys
import os
import json

IP = "127.0.0.1"
PORT = 1234
HEADERSIZE = 10

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((IP, PORT))
    server.listen()

    # accept client connection
    conn, addr = server.accept()
    print(f"Connection from {addr} successfull!\n")

    while True:
        
        # receive file name from client
        full_message = b''

        while True:
            
            try:
            
                header = conn.recv(HEADERSIZE)
            
            except:

                print("Connection from client ended!")

                sys.exit()
            
            else:

                if not header:
                    break 

                message_length = int(header.decode('utf-8'))

                while message_length - len(full_message) > 0:

                    message = conn.recv(HEADERSIZE)
                    full_message += message 
            
                break 

        file_name = full_message.decode('utf-8')

        error_message = None 

        response = None

        if file_name:

            print(f"Client wants file - {file_name}\n")
            
            # find file
            if os.path.exists(f'Server Files/{file_name}'):

                print(f"{file_name} found!\n")

                full_file = b''

                with open(f'Server Files/{file_name}', 'rb') as file:

                    while True:
                        bytes_read = file.read(HEADERSIZE)

                        if not bytes_read:
                            break 
                    
                        full_file += bytes_read


                full_file = full_file.decode('utf-8')

                response = {
                    "type": "response",
                    "code": 200,
                    "file": full_file
                }
            
            else:

                print(f"{file_name} does not exist!\n")

                # handle errors
                error_message = {
                    "type": "error",
                    "code": 404,
                    "text": "File not found"
                }

        else:

            print("No file name provided!\n")

            # handle errors
            error_message = {
                "type": "error",
                "code": 400,
                "text": "Please provide a filename"
            }

        # send file or error
        message = ''
        header = ''

        if error_message:
            
            message = json.dumps(error_message)
            header = json.dumps(f"{len(message):<{HEADERSIZE}}")

        else:

            message = json.dumps(response)
            header = json.dumps(f"{len(message):<{HEADERSIZE}}")


        message = header + message 

        conn.send(message.encode('utf-8'))

    # rinse repeat