import socket
import struct#a way to group several related variables into one place

PORT = 55551
HOST = '127.0.0.1'

def receive_file(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print(f"Server is listening on {host}:{port}")

        while True:
            client, address = server.accept()
            with client:
                print(f"Connected by {address}")

                # Receive the length of the file name
                file_name_length_data = client.recv(4)  # 4 bytes for length
                file_name_length = struct.unpack('I', file_name_length_data)[0]

                # Receive the file name
                file_name = client.recv(file_name_length).decode('utf-8')  # Decode the file name from bytes to string
                print(f"Receiving file: {file_name}")

                # Open the file for writing in binary mode
                with open(file_name, 'wb') as file:
                    while True:
                        data = client.recv(1024)  # Receive data from the socket
                        if not data:
                            break
                        file.write(data)  # Write the data to the file

                print(f"File '{file_name}' received successfully.")

if __name__ == "__main__":
    receive_file(HOST, PORT)
