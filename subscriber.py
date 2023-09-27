import settings
from SubscriberSocket import SubscriberSocket

print("Subscriber")

subscriber_socket = SubscriberSocket()
subscriber_socket.connect(settings.Settings.BROKER_HOST, settings.Settings.BROKER_PORT)

# if subscriber_socket.is_connected:

topic = input("\nEnter the topic to subscribe: ")

# subscriber_socket.close() --> pentru test in BrokerSocket.handle_client

# de adaugat in while true si pentru fiecare subscrube new thread

subscriber_socket.subscribe(topic)
subscriber_socket.receive_content()
