import psycopg2
from urllib.parse import urlparse
import pandas as pd

def pull_data():
    url = urlparse("postgres://user-reach:UJ9O8ArOclMuVqxM6J4isNOeYTyJXdWU@db.shuttle.rs:5432/db-reach")
    try:
        connection = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        print("Connection successful")

    except Exception as e:
        print(e)
        return None

    query = "SELECT * FROM smart_budgets WHERE user_id = 92"

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Fetch column names
        column_names = [desc[0] for desc in cursor.description]
        
        # Fetch all rows
        results = cursor.fetchall()
        
    except Exception as e:
        print(e)
        return None

    finally:
        if connection:
            connection.close()

    # Return data as DataFrame with column names
    return pd.DataFrame(results, columns=column_names)

# Pull data and display as DataFrame
df = pull_data()
if df is not None:
    print(df)
