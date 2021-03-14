import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os


def db_init():
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "./convbull-firebase-adminsdk-zfqmc-3a1d316ad1.json"

    # Use a service account
    cred = credentials.Certificate("./convbull-firebase-adminsdk-zfqmc-3a1d316ad1.json")
    firebase_admin.initialize_app(cred)

    db = firestore.Client()
    return db


def add_message_thread(db, msg_thread):
    doc_ref = db.collection(u"message-threads").document(msg_thread["id"])
    doc_ref.set(
        {
            u"x": msg_thread["x"],
            u"y": msg_thread["y"],
            u"message_thread_id": msg_thread["id"],
            u"messages": [],
        }
    )


def add_message(db, msg, msg_thread_id):
    doc_ref = db.collection(u"message-threads").document(msg_thread_id)
    doc_ref.update(
        {
            u"messages": firestore.ArrayUnion(
                [
                    {
                        u"user": msg["user"],
                        u"body": msg["body"],
                        u"timestamp": msg["timestamp"],
                    }
                ]
            )
        }
    )


def get_message_threads(db):
    # Then query for documents
    message_threads_ref = db.collection(u"message-threads")

    for doc in message_threads_ref.stream():
        print(u"{} => {}".format(doc.id, doc.to_dict()))
