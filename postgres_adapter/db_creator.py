import psycopg2

# Параметры подключения к вашему PostgreSQL серверу
host = "localhost"  # имя сервиса в Docker Compose
user = "username"
password = "password"
db_name = "name"
port = "5432"

# Подключение к базе данных
try:
    conn = psycopg2.connect(
        host=host, port=port, user=user, password=password, database=db_name
    )
    conn.autocommit = True

    # Создание курсора для выполнения операций с базой данных
    cursor = conn.cursor()

    # Создание таблицы
    create_table_query = """
    CREATE TABLE IF NOT EXISTS issues (
        id SERIAL PRIMARY KEY,
        name_issue VARCHAR(255),
        reason_issue VARCHAR(255),
        description TEXT
    );
    """
    cursor.execute(create_table_query)
    print("Таблица успешно создана")

    # Вставка тестовых данных
    insert_query = """
    INSERT INTO issues (name_issue, reason_issue, description)
    VALUES (%s, %s, %s);
    """
    data = [
        ("Issue 1", "Reason 1", "Description for Issue 1"),
        ("Issue 2", "Reason 2", "Description for Issue 2"),
        ("Issue 3", "Reason 3", "Description for Issue 3"),
    ]

    for record in data:
        cursor.execute(insert_query, record)
    print("Данные успешно вставлены")

except psycopg2.OperationalError as e:
    print(f"Ошибка подключения: {e}")
finally:
    # Закрытие соединения с базой данных, если оно было установлено
    if "conn" in locals() and conn is not None:
        cursor.close()
        conn.close()
