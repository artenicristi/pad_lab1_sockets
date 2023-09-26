import settings
from BrokerSocket import BrokerSocket

broker = BrokerSocket()

broker.begin(settings.Settings.BROKER_HOST, settings.Settings.BROKER_PORT)