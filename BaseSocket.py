import socket

import settings


class BaseSocket:
    is_connected = False

    def __init__(self, sock=None):
        self.__sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_socket(self):
        return self.__sock

    def connect(self, host, port):
        try:
            self.__sock.connect((host, port))
            print("Socket connected successfully")
            self.is_connected = True

        except (socket.error, OSError) as e:
            print(f"Socket connection failed: {e}")

    def send(self, data):
        try:
            self.__sock.send(data.encode('utf-8'))
            print("Data sent successfully")
        except (socket.error, OSError) as e:
            print(f"Failed to send data: {e}")

    def receive(self):
        while True:
            try:
                data = self.__sock.recv(settings.Settings.BUFFER_SIZE)

                if not data:
                    break

                print(f"Received content: {data.decode('utf-8')}\n")
            except (socket.error, OSError) as e:
                print(f"Failed to receive data: {e}")

    def close(self):
        try:
            self.__sock.close()
            self.is_connected = False
            print("Socket closed successfully")
        except (socket.error, OSError) as e:
            print(f"Failed to close socket: {e}")
