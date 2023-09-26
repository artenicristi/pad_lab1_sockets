from sqlalchemy.orm import sessionmaker
import SocketsDB
from SocketsDB import PayloadModel

Session = sessionmaker(bind=SocketsDB.engine)
session = Session()


class PayloadRepository:
    SUBSCRIBE = "subscribe@"
    CONTENT = "content"

    @staticmethod
    def add(type, topic, content):
        # try catch
        payload = PayloadModel(type, topic, content)
        session.add(payload)
        session.commit()

    @staticmethod
    def delete(payload):
        # try catch
        session.delete(payload)
        session.commit()

    @staticmethod
    def load():
        # try catch posibil sa nu trebuiasca deorece eroare nu prea putem avea
        # dar la insert si operatii de manipulare ar trebui de pus try/catch
        # limit size = ?? o constanta ceva
        # de verificat in worker mai intai daca in DB.payloads sunt inregistrari
        # de adaugat vreo metoda care scoate vreun count() poate din DB ca sa vad daca sunt inregistrari
        # sau se poate de lasat fara counter si mereu scoatem din db
        # si daca e array gol nu se intampla nimic oricum
        payloads = session.query(PayloadModel).limit(5)
        return payloads
