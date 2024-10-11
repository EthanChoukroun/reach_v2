import requests


def get_transactions(user):
    # Define the URL
    url = "https://reach.shuttleapp.rs/api/plaid/transactions"

    params = {
        "email": user # Example query parameter
    }

# Make a GET request
    response = requests.get(url, params=params)

    return response.text