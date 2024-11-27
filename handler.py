from KSockets import SimpleClient
import time
from threading import Thread
def packer(message: str):
    return {
        "purpose": "prompt",
        "data": message
    }
class Client_Handler:
    def __init__(self, client: SimpleClient, auth, name) -> None:
        self.client = client
        self.client.send({"name": name, "cli-auth": auth})
        self.metadata = self.client.receive(unpack_exc_detailed=True)
        self._backlog = None
        self.active = True

    def receive_loop(self):
        "Should be on a threaded environment"
        try:
            while True:
                data = self.client.receive(unpack_exc_detailed=True)
                if not data:
                    self.client.close()
                    print("\n[Client Handler] Receive loop ended due to empty or invalid data, you may have lost connection")
                    self.active = False
                    break
                elif not self._backlog:
                    self._backlog = data
                else:
                    #Very rare event
                    while self._backlog != None: time.sleep(0.5)
                    self._backlog = data
        except KeyboardInterrupt:
            print("\nStopped Thread! Keyboard Interrupt!")
        except ConnectionAbortedError:
            print("\nStopped Thread! Connection Aborted!")
        except OSError:
            print("\nStopped Thread! Connection Aborted!")

    def consume_data(self):
        "Receive the most recent backlog"
        while self._backlog == None: time.sleep(0.5)
        backlog = self._backlog
        self._backlog = None
        return backlog

    def start(self):
        "Starts the receive loop"
        Thread(target=self.receive_loop).start()

    def send_prompt(self, message):
        message_full = packer(message=message)
        self.client.send(message_full)

    def close(self):
        self.client.close()