import socket


class BaseSocket:
    def __init__(self):
        self.__sock = None

    def get_socket(self):
        return self.__sock

    def connect(self, host, port):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect((host, port))
            print("Socket connected successfully")
        except (socket.error, OSError) as e:
            print(f"Socket connection failed: {e}")

    def send(self, data):
        try:
            self.__sock.send(data.encode('utf-8'))
            print("Data sent successfully")
        except (socket.error, OSError) as e:
            print(f"Failed to send data: {e}")

    def receive(self, buffer_size=1024):
        try:
            if self.__sock:
                data = self.__sock.recv(buffer_size)
                if data:
                    print(f"Received data: {data.decode('utf-8')}")
                else:
                    print("No data received.")
            else:
                print("Socket not connected.")
        except (socket.error, OSError) as e:
            print(f"Failed to receive data: {e}")

    def close(self):
        try:
            self.__sock.close()
            print("Socket closed successfully")
        except (socket.error, OSError) as e:
            print(f"Failed to close socket: {e}")
