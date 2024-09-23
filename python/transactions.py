import requests


def get_transactions(user):
    # Define the URL
    url = "http://localhost/api/plaid/transactions"

    params = {
        "email": user # Example query parameter
    }

# Make a GET request
    response = requests.get(url, params=params)

    print(response.text)