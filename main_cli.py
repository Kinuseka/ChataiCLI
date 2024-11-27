from KSockets.secure import wrap_secure
from KSockets import SimpleClient
from handler import Client_Handler
import sys, os
from termcolor import colored
import time
import json
IP = None
PORT = None
UPASS = None
DEFAULT_NAME = "Shizu"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def read(response, expected):
    if response["purpose"] == expected:
        return True
    elif response["purpose"] == "error":
        print("[Error] %s" % response["data"])
        return False
    else:
        return False

def load_config():
    global IP, PORT, UPASS
    with open(resource_path("shipping_config.json"), "r") as f:
        config = json.load(f)
        if config.get('Server', None) and config.get('Port', None):
            IP = config['Server']
            UPASS = config.get("Password", None)
            try:
                PORT = int(config['Port'])
            except ValueError:
                return 0
            return 1
        else:
            print(colored("Config is INVALID", "red"))
            return 0
        
def main(client: Client_Handler):
    data = client.metadata['data']
    print(colored("====", "blue"))
    print(f"{colored('Server Version:', 'green')} {colored(data['server_version'],'yellow')}")
    print(f"{colored('Model:', 'green')} {colored(data['model'],'yellow')}")
    print(colored("====", "blue"))
    while True:
        prompt = input(colored("Enter prompt: ", "cyan"))
        if not prompt: continue
        print("Sending...", end="\r")
        client.send_prompt(prompt)
        received = client.consume_data()
        if read(received, "waiting"):
            print("AI thinking...", end="\r")
        elif read(received, "ready"):
            print("AI ready for prompt")
            continue
        else:
            print("[Error] Remote returned invalid message")
            continue
        response = client.consume_data()
        if read(response, "reply"):
            print(colored("[AI]: ", "light_yellow"), colored(response['data'], "white"))

if __name__ == "__main__":
    try:
        if not load_config():
            print("==Closing in 5 seconds==")
            time.sleep(5)
            sys.exit()
        print("Chatai (CLI) V1.0")
        print("IP: %s\nPORT: %s" % (IP, PORT))
        client = SimpleClient((IP,PORT))
        client = wrap_secure(SimpleClient((IP, PORT)), certpath=resource_path("cert/certificate_file.crt"))
        client.connect()
        name = input(f"Enter name ({DEFAULT_NAME}): ") or DEFAULT_NAME
        custom_handler = Client_Handler(client, auth=UPASS,name=name)
        if custom_handler.metadata: #As per protocol, No metadata means rejected
            custom_handler.start()
            main(client=custom_handler)
        else:
            print(colored("Rejected from server, check your connection or your password is correct", "red"))
        # daeThread.
    except KeyboardInterrupt:
        custom_handler.close()