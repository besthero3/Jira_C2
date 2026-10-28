import os
import socket
from ipaddress import ip_address

import requests
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

    print(team_num)
    print(epic_ID)
    print(ip_addr)

def init():
    pass

def main():
    global url

    response = requests.get(url=url, headers=headers, auth=auth, timeout=10)
    print(str(response.status_code))
    ip_mapping()


if __name__ == '__main__':
    main()