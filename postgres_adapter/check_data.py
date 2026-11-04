import psycopg2


def fetch_all_data():
    connection = None
    try:
        # Connection parameters for your PostgreSQL server
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="name",
            user="username",
            password="password",
        )

        cursor = connection.cursor()

        # SQL-query to select all data
        fetch_query = "SELECT * FROM issues;"
        cursor.execute(fetch_query)

        # Fetch and print all rows
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL", error)
    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection closed")


# Call the function
fetch_all_data()
