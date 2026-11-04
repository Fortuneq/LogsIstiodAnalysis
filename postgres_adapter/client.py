import requests


def add_issue(name_issue, reason_issue, description):
    url = "http://localhost:5002/add_issue"
    data = {
        "name_issue": name_issue,
        "reason_issue": reason_issue,
        "description": description,
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to add issue", "status_code": response.status_code}


def get_issue(issue_id):
    response = requests.get(f"http://localhost:5002/check_issue/{issue_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Issue not found or server error"}


def download_feature_lines():
    url = "http://localhost:5002/analyze_issue"
    response = requests.post(url)
    if response.status_code == 200:
        with open("downloaded_feature_lines.txt", "wb") as file:
            file.write(response.content)
        print("File uploaded successfully.")
        return True
    else:
        print(f"File upload error: {response.status_code}")
        return False


# Usage example
print(
    add_issue(
        "Test Issue", "Test Reason", "This is a test description"
    )  # Add a new incident
)
print(get_issue(1))  # Get information about the incident with ID 1
download_feature_lines()  # Upload the feature_lines.txt
