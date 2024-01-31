from pymongo.mongo_client import MongoClient
import yaml

with open("src/config.yaml", "r") as config:
    config_data = yaml.safe_load(config)


# url of the mongodb atas to connect to the server
url = config_data['config']['MongoDB_URL']

class Mongodb:
    def __init__(self):
        # Create a new client and connect to the server
        self.client = MongoClient(url)

    # Function to store the youtube data 
    def store_temp_info(self,channel_details):

        db = self.client["youtube_temp_data"]
        collection_name = channel_details['channel_name']
        collection = db[collection_name]
        collection.insert_one(channel_details)
        return()
    
    def collection_list(self, database):
        
        db = self.client[database]
        collection = db.list_collection_names()
        if collection:
            return(collection)
        else:
            return(False)
        
    
    def delete_temp_data(self):

        db = self.client["youtube_temp_data"]        
        collections = db.list_collection_names()
        if len(collections) > 0:
            for collection in collections:
                db.drop_collection(collection)
            return()
        
    def read_collection(self, channel_name):
        db = self.client["youtube_temp_data"] 
        collection = db[channel_name]
        documents = collection.find()
        for document in documents:
            channel_detail = document
        return(channel_detail)

    def add_document(self, data):
        db = self.client["youtube_data_harversting"]
        collection_name = data['channel_info']['channel_name']
        collection = db[collection_name]
        collection.insert_one(data)
        return()
    
    def delete_document(self, document):
        db = self.client["youtube_data_harversting"]
        collection_name = document
        db[collection_name].drop()
        return()