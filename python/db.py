import psycopg2
from urllib.parse import urlparse
import pandas as pd

def pull_data():
    url = urlparse("postgres://user-reach:UJ9O8ArOclMuVqxM6J4isNOeYTyJXdWU@db.shuttle.rs:5432/db-reach")
    try:
        connection = psycopg2.connect(
            dbname=url.path[1:],
            user = url.username,
            password = url.password,
            host = url.hostname,
            port = url.port
        )
        print("connection successful")

    except Exception as e:
        print(e)


    query = "SELECT * FROM transactions"

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    if connection:
        connection.close()

    return results
# print(results)


tr = pull_data()
df = pd.DataFrame(tr)
print(df.iloc[0])


