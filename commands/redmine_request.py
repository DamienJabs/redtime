import requests

def redmine_request(redmine_url, redmine_api_key, endpoint, method="GET", data=None):
    headers = {"X-Redmine-API-Key": redmine_api_key}
    url = f"{redmine_url}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        else:
            raise ValueError("Unsupported HTTP method")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"HTTP request failed: {e}")
        exit(1)
    return response
