import psycopg2


def fetch_all_data():
    connection = None
    try:
        # Параметры подключения к вашему PostgreSQL серверу
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="name",
            user="username",
            password="password",
        )

        cursor = connection.cursor()

        # SQL-запрос для выборки всех данных
        fetch_query = "SELECT * FROM issues;"
        cursor.execute(fetch_query)

        # Получение и вывод всех строк
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к PostgreSQL", error)
    finally:
        # Закрытие соединения
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# Вызов функции
fetch_all_data()
