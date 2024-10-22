import socket
import threading
import psycopg2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9123)

server_socket.bind(server_address)

server_socket.listen(1)
client_sockets = []
def db_connect():
    connection = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='qwerty123',
        host='localhost',
        port='5432'
    )
    return connection

def handle_client(client_socket):
    user_db = None;
    while True:
        client_socket.send("Введите логин: ".encode())
        data = client_socket.recv(1024)
        login = data.decode()
        client_socket.send("Введите пароль: ".encode())
        data = client_socket.recv(1024)
        password = data.decode()
        cursor = (db_connect()).cursor()
        cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
        user_db = cursor.fetchone()
        if user_db[3] == password:
            cursor.execute("SELECT id FROM messages WHERE from_id = %s OR to_id = %s", (user_db[0], user_db[0]))
            messages = cursor.fetchall()
            for message in messages:
                cursor.execute("SELECT * FROM get_message_datails(%s)", (message[0], ))
                msg = cursor.fetchone()
                msg = msg[0]+" "+msg[1]+" "+msg[2]
                client_socket.send(msg.encode())
            break
        else:
            client_socket.send("Неправильный логин или пароль\n ".encode())

    while True:
        client_socket.send("Введите логин$получателя и сообщение: ".encode())
        data = client_socket.recv(1024)
        login_and_message = data.decode().split('$')
        print(f"Пользователь прислал сообщение: {data.decode()}")
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE login = %s", (login_and_message[0], ))
        receiver_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO messages (to_id, from_id, msg) VALUES (%s, %s, %s)", (receiver_id, user_db[0], login_and_message[1]))
        conn.commit()
        for socket in client_sockets:
            if socket != client_socket:
                socket.send(data)

while True:
    client_socket, client_address = server_socket.accept()
    print("Клиент подключился")
    client_sockets.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()