import socket


class PublisherSocket:
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

    def send(self, data):
        try:
            self.__socket.send(data)
        except Exception as e:
            print(f"Failed to send message {e}")