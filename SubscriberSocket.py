import json
import socket
import threading

from PayloadRepository import PayloadRepository, PayloadModel


class SubscriberSocket:
    __socket = None
    is_connected = False

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, broker_host, broker_port):
        try:
            self.__socket.connect((broker_host, broker_port))
            print("Socket connected successfully")
            self.is_connected = True
        except Exception as e:
            print(f"Socket connection failed {e}")

    def subscribe(self, topic):
        payload_data = PayloadModel.as_dict(PayloadRepository.SUBSCRIBE, topic)

        try:
            self.__socket.send(json.dumps(payload_data).encode('utf-8'))
        except Exception as e:
            print(f"Failed to send message {e}")

    def print_message(self, socket):
        while True:
            data = socket.recv(1024)

            # de verificat dupa content length mai bine
            if not data:
                # sau daca apare eroare de conectare, trebuie de vazut cand
                break

            print(f"Received content: {data.decode('utf-8')}\n")

    def receive(self):
        print(f"Waiting for data ... {self.__socket.getsockname()}")
        host, port = self.__socket.getsockname()

        waiting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        waiting_socket.bind((host, int(port)))
        waiting_socket.listen(5)

        while True:
            server_socket, server_address = waiting_socket.accept()
            thread = threading.Thread(target=self.print_message, args=(server_socket,))
            thread.start()



