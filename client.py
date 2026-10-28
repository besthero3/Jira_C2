import datetime
import os
import socket
import time
from time import timezone
from datetime import datetime, timezone


import requests
import schedule
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
email =  os.getenv('EMAIL')
token = os.getenv('API_TOKEN')
url = os.getenv('BASE_URL')
project_key = os.getenv('PROJECT_KEY')
board_id = os.getenv('BOARD_ID')

pitwall_IP = os.getenv('pitwall_IP')
teamradio_IP = os.getenv('teamradio_IP')
transporters_IP = os.getenv('transporters_IP')
stewards_IP =  os.getenv('stewards_IP')

command_EPIC_ID = "JC-9"

# variables
global team_num
global epic_ID
global ip_addr
issue_key = None

#basic configuration
auth = HTTPBasicAuth(
    email,
    token
)

headers = {
    "Accept": "application/json"
}

# gets the IP address and team number and epic
def ip_mapping():
    global team_num
    global epic_ID
    global ip_addr

    global pitwall_IP
    global teamradio_IP
    global transporters_IP
    global stewards_IP

    #gets IP of this host
    hostname = socket.gethostname()
    IP_Address = socket.gethostbyname(hostname)

    ip_addr = IP_Address

    #Hardcoded IP Mapping:
    IPsplitByOctet = IP_Address.split('.')

    # -1 is a placeholder for all of these cases
    # IP mappings for each host group
    pitwall_IP_octet =       pitwall_IP.split('.')
    teamradio_IP_octet =     teamradio_IP.split('.')
    transporters_IP_octet =  transporters_IP.split('.')
    stewards_IP_octet =      stewards_IP.split('.')

    pitwall_EPIC_ID = "JC-1"
    teamradio_EPIC_ID = "JC-3"
    transporters_EPIC_ID = "JC-4"
    stewards_EPIC_ID = "JC-5"
    test_epic_ID = "JC-12"

    #Pitwall
    if IPsplitByOctet[0] == pitwall_IP_octet[0] and IPsplitByOctet[2] == pitwall_IP_octet[2] and IPsplitByOctet[3] == pitwall_IP_octet[3]:
        team_num = IPsplitByOctet[1]
        epic_ID = pitwall_EPIC_ID

    #teamradio
    elif IPsplitByOctet[0] == teamradio_IP_octet[0] and IPsplitByOctet[2] == teamradio_IP_octet[2] and IPsplitByOctet[3] == teamradio_IP_octet[3]:
        team_num = IPsplitByOctet[1]
        epic_ID = teamradio_EPIC_ID

    #transporters
    elif IPsplitByOctet[0] == transporters_IP_octet[0] and IPsplitByOctet[1] == transporters_IP_octet[1] and IPsplitByOctet[3] == transporters_IP_octet[3]:
        team_num = IPsplitByOctet[2]
        epic_ID = transporters_EPIC_ID

    #stewards
    elif IPsplitByOctet[0] == stewards_IP_octet[0] and IPsplitByOctet[1] == stewards_IP_octet[1] and IPsplitByOctet[3] == stewards_IP_octet[3]:
        team_num = IPsplitByOctet[2]
        epic_ID = stewards_EPIC_ID

    #LOCAL TESTING
    else:
        team_num = IPsplitByOctet[1]
        epic_ID = test_epic_ID


def callback():
    global url
    global team_num
    global epic_ID
    global ip_addr
    global issue_key

    if issue_key is None:
        return

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.000%z"
    )

    payload = {
        "fields": {
            "customfield_10049": timestamp
        }
    }

    requests.put(url=f"{url}/rest/api/3/issue/{issue_key}", json=payload, headers=headers, auth=auth, timeout=20)

def init():
    #have to check if exists already

    global url
    global team_num
    global epic_ID
    global ip_addr
    global project_key
    global issue_key

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.000%z"
    )
    existing_host = False

    team_num = int(team_num)

    #JQL vs API for customfield stuff
    search = {"jql": f"project = {project_key} AND cf[10050] = {team_num}",
              "fields": ["summary", "customfield_10048"]}

    response = requests.post(url=f"{url}/rest/api/3/search/jql", json=search, headers=headers, auth=auth, timeout=20)

    print(response.json())
    for IP in response.json()["issues"]:
        #JSON custom field format different than JQL
        #.get prevents key error
        if IP["fields"].get("customfield_10048") == str(ip_addr):
            existing_host = True
            issue_key = IP["key"]
            print("Found Original Story " + issue_key)

            #updates the time
            callback()
            break

    if existing_host == False:
        payload = {
            "fields": {
                "project": {"key": project_key},
                "parent": {"key": epic_ID},
                "issuetype": {"name": "Task"},
                "summary": str(ip_addr),

                "customfield_10048": str(ip_addr),
                "customfield_10050": int(team_num),
                "customfield_10049": timestamp
            }
        }

        response = requests.post(url=f"{url}/rest/api/3/issue", json=payload, headers=headers, auth=auth, timeout=20)

        #key is what we need, BUT have to make sure there is not already something with our ip address as title
        print(response.json()['key'])
        print(response.text)
        print(response.status_code)

def main():
    global issue_key
    ip_mapping()

    init()
    schedule.every(4).to(5).minutes.do(callback)

    #keeps loop alive
    while True:
        schedule.run_pending()
        time.sleep(120)

if __name__ == '__main__':
    main()