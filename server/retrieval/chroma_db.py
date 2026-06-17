#set a session wide init for vector db.
import chromadb
from flask import current_app
#add logging
def init_vector_db():
    collection_name = "NarrativeOS"
    chroma_client = chromadb.PersistentClient(path='server/retrieval/chroma.sqlite3')
    #create a collection
    collection = chroma_client.get_or_create_collection(name=collection_name)
    current_app.config["CHROMA_DB"] = collection
    # return collection #***DELETE THIS

def get_vector_db():
    return current_app.config["CHROMA_DB"]