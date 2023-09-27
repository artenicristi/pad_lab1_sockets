import json
import threading
import time

import settings
from BaseSocket import BaseSocket
from ConnectionRepository import ConnectionRepository
from PayloadRepository import PayloadRepository


def worker_messages():
    while True:
        time.sleep(5)
        print("Worker messages started:\n")

        payloads = PayloadRepository.load()

        for payload in payloads:
            topic = payload.topic
            connections = ConnectionRepository.get_by_topic(topic)

            if not connections.count():
                continue

                # ?????????????????
                # CERTIFICATELE CAR && KEY
                # ?????????????????

            for conn in connections:
                subscriber_socket = BaseSocket()
                print(f"Trying to connect to {conn.host}:{conn.port} to send {payload.content}")
                subscriber_socket.connect(conn.host, int(conn.port))
                if not subscriber_socket.is_connected:
                    continue
                subscriber_socket.send(payload.content)
                subscriber_socket.close()

            PayloadRepository.delete(payload)


def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.get_socket().recv(settings.Settings.BUFFER_SIZE)
            if not data:
                print(f"Connection closed by {client_address}")
                ConnectionRepository.delete_by_host_port(client_address)
                break

            payload_data = json.loads(data.decode('utf-8'))
            print(f"Received JSON object: {payload_data} from {client_address}")

            if payload_data['type'] == PayloadRepository.SUBSCRIBE:
                ConnectionRepository.add(payload_data['topic'], *list(client_address))
            else:
                PayloadRepository.add(payload_data['type'], payload_data['topic'], payload_data['content'])
        except ConnectionResetError as e:
            ConnectionRepository.delete_by_host_port(client_address)
            print(f"Connection was forcibly closed : {e}")
            break
        except Exception as e:
            print(f"Error in handle_client: {e}")
            break

    client_socket.close()


class BrokerSocket(BaseSocket):
    def __init__(self):
        super().__init__()

    def begin(self, broker_host, broker_port):
        super().get_socket().bind((broker_host, broker_port))
        super().get_socket().listen(settings.Settings.MAX_PENDING_CONNECTIONS)

        print(f"Broker listening on {broker_host}:{broker_port}")

        worker_thread = threading.Thread(target=worker_messages)
        worker_thread.start()

        while True:
            client_socket, client_address = super().get_socket().accept()
            client_thread = threading.Thread(target=handle_client,
                                             args=(BaseSocket(client_socket), client_address))
            client_thread.start()
