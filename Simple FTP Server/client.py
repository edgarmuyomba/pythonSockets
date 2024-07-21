import socket 
import sys
import json

IP = "127.0.0.1"
PORT = 1234
HEADERSIZE = 10

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

    client.connect((IP, PORT))

    while True:

        file_name = input("Which file? ")

        if file_name == "None":

            print("\n Connection Terminated!\n")
            
            sys.exit()

        # construct and send the request
        header = f"{len(file_name):<{HEADERSIZE}}"

        message = header + file_name

        client.send(message.encode('utf-8'))

        # receive the response

        while True:

            full_response = b''

            while True:

                header = client.recv(12)

                if not header:

                    break 
                    
                message_length = int(json.loads(header.decode('utf-8')))

                while message_length - len(full_response) > 0:

                    message = client.recv(HEADERSIZE)

                    full_response += message 
                
                break 
            
            full_response = json.loads(full_response.decode('utf-8'))

            if full_response['type'] == "error":

                print(f'{full_response['text']}\n')

                if full_response['code'] == 400:

                    break 

                elif full_response['code'] == 404:

                    break 
            
            else:
                
                print(f"Successfully received {file_name}\n")

                full_file = full_response['file']

                # save the file

                with open(f'Client Files/{file_name}', 'w') as file:

                    file.write(full_file)
                
                break

        # rinse repeat