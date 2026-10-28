import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
email =  os.getenv('EMAIL')
token = os.getenv('API_TOKEN')
url = os.getenv('BASE_URL')

#basic configuration
auth = HTTPBasicAuth(
    email,
    token
)

headers = {
    "Accept": "application/json"
}


def main():
    global url

    response = requests.get(url=url, headers=headers, auth=auth, timeout=10)
    print(response.text + " " +  str(response.status_code))


if __name__ == '__main__':
    main()