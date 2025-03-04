import requests
import time
import os
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s | %(message)s', datefmt='%d-%m-%Y %I:%M:%S' ,filename='server.log', encoding='utf-8', level=logging.DEBUG)


client_hosts = ["http://host1:5000", "http://host2:5000", "http://host3:5000"]
STATE_FILE = "current_host.txt"


def load_last_host():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def save_last_host(index):
    with open(STATE_FILE, "w") as f:
        f.write(str(index))

current_index = load_last_host()

while True:
    if current_index >= len(client_hosts):
        current_index = 0

    host = client_hosts[current_index]

    try:
        response = requests.get(f"{host}/status")
        status = response.json().get("status")

        if status == "WAIT":
            logging.info(f"Sending START message to {host}")
            requests.post(f"{host}/run")
            save_last_host(current_index)

        elif status == "START":
            logging.info(f"{host} is still working")

        elif status == "DONE":
            logging.info(f"Host {host} finished his task, switching to the nex one. ")
            current_index += 1
            save_last_host(current_index)

    except requests.exceptions.ConnectionError:
        logging.error(f"No connection with {host}, skipping...")

    time.sleep(2)
