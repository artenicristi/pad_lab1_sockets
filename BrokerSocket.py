import json
import socket
import threading
import time

from ConnectionRepository import ConnectionRepository
from PayloadRepository import PayloadRepository


# pot sa adaug in clasa noua, de vazut
def worker_messages():
    while True:
        # de lasat time sleep-ul ca sa simulez procesul la un interval
        time.sleep(5)
        print("Worker messages started:\n")

        payloads = PayloadRepository.load()

        for payload in payloads:
            topic = payload.topic
            connections = ConnectionRepository.get_by_topic(topic)

            for conn in connections:
                subscriber_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print(f"Trying to connect to {conn.host}:{conn.port} to send {payload.content}")
                try:
                    subscriber_socket.connect((conn.host, int(conn.port)))
                except ConnectionRefusedError as e:
                    print(f"Subscriber stoped: {e}")
                    continue
                subscriber_socket.send(payload.content.encode('utf-8'))
                subscriber_socket.close()

            PayloadRepository.delete(payload)

class BrokerSocket:
    __socket = None
    MAX_PENDING_CONNECTIONS = 5
    BUFFER_SIZE = 1024

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                # poate aici de prins mesaul exit pentru a sterge conexiunea
                data = client_socket.recv(self.BUFFER_SIZE)

                # de verificat dupa content length mai bine
                if not data:
                    print(f"Connection closed by {client_address}")
                    # delete from connections storage
                    # sau daca apare eroare de conectare, trebuie de vazut cand
                    break

                payload_data = json.loads(data.decode('utf-8'))
                print(f"Received JSON object: {payload_data} from {client_address}")

                # de adaugat mai intai transient intr-o coada ceva si pe urma de facut
                # un worker care din timp in timp sa adauge in DB
                if payload_data['type'] == PayloadRepository.SUBSCRIBE:
                    ConnectionRepository.add(payload_data['topic'], *list(client_address))
                else:
                    PayloadRepository.add(payload_data['type'], payload_data['topic'], payload_data['content'])
            except Exception as e:
                print(f"Error in handle_client: {e}")
                break

        client_socket.close()

    def begin(self, broker_host, broker_port):
        self.__socket.bind((broker_host, broker_port))
        self.__socket.listen(self.MAX_PENDING_CONNECTIONS)

        print(f"Broker listening on {broker_host}:{broker_port}")

        worker_thread = threading.Thread(target=worker_messages)
        worker_thread.start()

        while True:
            client_socket, client_address = self.__socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
#             sa verific daca dupa thread.start() intr-adevar se porneste thread nou si printul cu test de mai jos se executa in paralel
#             print("test test")




