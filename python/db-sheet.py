from flask import Flask, request, jsonify
import psycopg2
from urllib.parse import urlparse

# Initialize Flask app
app = Flask(__name__)

# Database connection details
DB_URL = "postgres://user-reach:UJ9O8ArOclMuVqxM6J4isNOeYTyJXdWU@db.shuttle.rs:5432/db-reach"

def pull_data(user_id=None, table_name=None):
    """
    Pulls data from the database based on user_id and table_name.

    Args:
        user_id (str or None): The user ID to filter by (or None for all).
        table_name (str): The database table name ("transactions" or "smart_budget").

    Returns:
        list of dict: The result rows as a list of dictionaries.
    """
    if table_name not in ["transactions", "smart_budgets"]:
        raise ValueError("Invalid table name. Must be 'transactions' or 'smart_budgets'.")

    # Parse DB URL
    url = urlparse(DB_URL)
    connection = psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    # Build the query
    if table_name == 'transactions':
        query = "SELECT created_at, amount, date, id, transaction_id, updated_at, user_id FROM transactions"
    else:
        query = f"SELECT * FROM {table_name}"
    if user_id and user_id.lower() != "all":
        query += f" WHERE user_id = {user_id}"

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query)
        colnames = [desc[0] for desc in cursor.description]  # Get column names
        rows = cursor.fetchall()  # Fetch all rows

    # Close the connection
    connection.close()

    # Convert rows to list of dicts
    results = [dict(zip(colnames, row)) for row in rows]
    return results

@app.route('/get_data', methods=['GET'])
def get_data():
    """
    API endpoint to fetch data from the database.

    Query Parameters:
        user_id (optional): The user ID to filter by (or 'all' for all users).
        table_name (required): The database table to query ("transactions" or "smart_budget").

    Returns:
        JSON response containing the data or an error message.
    """
    user_id = request.args.get('user_id', 'all')  # Default to 'all'
    table_name = request.args.get('table_name')

    if not table_name:
        return jsonify({"error": "table_name parameter is required"}), 400

    try:
        data = pull_data(user_id=user_id, table_name=table_name)
        return jsonify({"data": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
