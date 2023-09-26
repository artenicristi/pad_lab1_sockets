import settings
from SubscriberSocket import SubscriberSocket

print("Subscriber")

subscriber_socket = SubscriberSocket()
subscriber_socket.connect(settings.Settings.BROKER_HOST, settings.Settings.BROKER_PORT)

topic = input("\nEnter the topic to subscribe: ")
subscriber_socket.subscribe(topic)

subscriber_socket.receive()
