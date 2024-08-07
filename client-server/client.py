import socket
import os
import tkinter as tk
from tkinter import filedialog
import struct

PORT = 55551
HOST = '127.0.0.1'

def open_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All Files", "*.*"), ("Text files", "*.txt")]
    )

    if file_path:
        with open(file_path, 'rb') as file:
            file_contents = file.read()
        print("File contents:", file_contents[:100])  # Print the first 100 bytes for debugging
        return file_contents, os.path.basename(file_path)
    
    return None, None

def send_file(host, port, file_contents, file_name):
    if file_contents is None:
        print("No file contents to send.")
        return
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            
            # Send the length of the file name
            file_name_length = len(file_name)
            s.send(struct.pack('I', file_name_length))
            
            # Send the file name
            s.send(file_name.encode('utf-8'))
            
            # Send the file contents
            s.sendall(file_contents)
            
            # Optionally receive a response from the server
            data = s.recv(1024)
            print(f"Received {data!r}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_contents, file_name = open_file()
    if file_contents and file_name:
        send_file(HOST, PORT, file_contents, file_name)
