import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 9123))
def receive_message():
    while True:
        response = client_socket.recv(1024)
        print(response.decode())

def send_message():
        msg = input()
        client_socket.send(msg.encode())

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()


while True:
    send_message()