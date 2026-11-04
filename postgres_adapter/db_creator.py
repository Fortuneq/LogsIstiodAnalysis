import psycopg2

# Connection parameters for your PostgreSQL server
host = "localhost"  # service name in Docker Compose
user = "username"
password = "password"
db_name = "name"
port = "5432"

# Connect to the database
try:
    conn = psycopg2.connect(
        host=host, port=port, user=user, password=password, database=db_name
    )
    conn.autocommit = True

    # Create a cursor for database operations
    cursor = conn.cursor()

    # Create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS issues (
        id SERIAL PRIMARY KEY,
        name_issue VARCHAR(255),
        reason_issue VARCHAR(255),
        description TEXT
    );
    """
    cursor.execute(create_table_query)
    print("Table created successfully")

    # Insert test data
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
    print("Data inserted successfully")

except psycopg2.OperationalError as e:
    print(f"Connection error: {e}")
finally:
    # Close the database connection if it was established
    if "conn" in locals() and conn is not None:
        cursor.close()
        conn.close()
