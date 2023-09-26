import json

import settings
from PayloadRepository import PayloadRepository
from PublisherSocket import PublisherSocket
from SocketsDB import PayloadModel

print("Publisher")

publisher_socket = PublisherSocket()
publisher_socket.connect(settings.Settings.BROKER_HOST, settings.Settings.BROKER_PORT)

if publisher_socket.is_connected:
    while True:
        topic = input("\nEnter topic: ").lower().strip()
        content = input("Enter content: ")
        payload_data = PayloadModel.as_dict(PayloadRepository.CONTENT, topic, content)

        publisher_socket.send(json.dumps(payload_data).encode('utf-8'))
        input("Press enter to add new message")
