import json
import threading

import settings
from BaseSocket import BaseSocket
from PayloadRepository import PayloadRepository, PayloadModel


class SubscriberSocket(BaseSocket):

    def __init__(self):
        super().__init__()

    def subscribe(self, topic):
        payload_data = PayloadModel.as_dict(PayloadRepository.SUBSCRIBE, topic)
        super().send(json.dumps(payload_data))

    def print_message(self, socket):
        socket.receive()

    def receive_content(self):
        host, port = super().get_socket().getsockname()
        print(f"Waiting for content at ... {host}:{port}")

        binded_socket = BaseSocket()
        binded_socket.get_socket().bind((host, int(port)))
        binded_socket.get_socket().listen(settings.Settings.MAX_PENDING_CONNECTIONS)

        while True:
            accepted_socket, server_address = binded_socket.get_socket().accept()
            thread = threading.Thread(target=self.print_message, args=(BaseSocket(accepted_socket),))
            thread.start()
