import psycopg2

# name = input("Введите имя: ")
login = input("Логин: ")
# password = input("Пароль: ")

try:
    connection = psycopg2.connect(
        dbname = 'test_db',
        user = 'postgres',
        password = 'qwerty123',
        host = 'localhost',
        port = '5432'
    )
    cursor = connection.cursor()
    print("Соединение с БД успешно установлено")
    # Удаление
    data = (login, )
    cursor.execute("DELETE FROM users WHERE login = %s", data)
    connection.commit()
    # Изменение
    # data = (name, login)
    # cursor.execute("UPDATE users SET name = %s WHERE login = %s", data)
    # connection.commit()
    # Чтение
    # cursor.execute("SELECT * FROM users")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row[0], row[1], row[2], row[3])
    # Вставка
    # data = (name, login, password)
    # cursor.execute(f"INSERT INTO users (name, login, pass) VALUES (%s, %s, %s)", data)
    # connection.commit()

except Exception as e:
    print(f"Ошибка: {e}")