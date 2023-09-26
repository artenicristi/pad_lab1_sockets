import threading
import time

from sqlalchemy.orm import sessionmaker
import SocketsDB
from SocketsDB import ConnectionModel
from sqlalchemy.exc import IntegrityError

Session = sessionmaker(bind=SocketsDB.engine)
session = Session()

session_lock = threading.Lock()


class ConnectionRepository:

    @staticmethod
    def add(topic, host, port):
        with session_lock:
            try:
                print("Before sleep in add()")
                time.sleep(5)
                connection = ConnectionModel(topic, host, port)
                session.add(connection)
                session.commit()
            except IntegrityError as e:
                print(f"Failed to add new connection: {e.statement}")
                session.rollback()

    @staticmethod
    def get_by_topic(topic):
        with session_lock:
            print("Before sleep in get_by_topic()")
            time.sleep(5)
            connections = session.query(ConnectionModel).filter(ConnectionModel.topic == topic)
            return connections
