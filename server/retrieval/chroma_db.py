#set a session wide init for vector db.
import chromadb
from flask import current_app
#add logging
def init_vector_db():
    current_app.logger.info("Intializing vector DB retrieving persistent storage")
    collection_name = "NarrativeOS"
    try: 
        chroma_client = chromadb.PersistentClient(path='server/retrieval/persistent-client/')
        current_app.logger.info(chroma_client.list_collections())
        #create a collection
        collection = chroma_client.get_collection(name=collection_name)
        if collection is None or collection.count()==0:
            msg = f"Cannot retrieve collection named or empty collection {collection_name}, {collection} - {collection.count()}"
            current_app.logger.error(msg)
        current_app.config["CHROMA_DB"] = collection
        # return collection #***DELETE THIS
    except Exception as e:
        current_app.logger.error(str(e))
        raise RuntimeError("Failed Loading Chroma Collection") 
def get_vector_db():
    return current_app.config["CHROMA_DB"]