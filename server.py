import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9123)

server_socket.bind(server_address)

server_socket.listen(1)
client_sockets = []
def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        print(f"Пользователь прислал сообщение: {data.decode()}")
        for socket in client_sockets:
            if socket != client_socket:
                socket.send(data)

while True:
    client_socket, client_address = server_socket.accept()
    print("Клиент подключился")
    client_sockets.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()