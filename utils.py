import requests

def graphql_query(url, query, headers=None):
    payload = {"query": query}
    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if headers:
        default_headers.update(headers)

    response = requests.post(url, json=payload, headers=default_headers)
    response.raise_for_status()
    return response.json()
