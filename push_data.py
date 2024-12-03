import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logger_config.logger import logging

from dotenv import load_dotenv
load_dotenv()

Mongo_db_url = os.getenv("MongoDB_url")


ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(sefl,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_into_mongo(self,records,database,collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection
            
            self.mongo_client = pymongo.MongoClient(Mongo_db_url)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "ADHASAI"
    COLLECTION = "NetworkData"
    networkobj = NetworkDataExtract()
    RECORDS = networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(RECORDS)
    no_of_records = networkobj.insert_data_into_mongo(RECORDS,DATABASE,COLLECTION)
    print(no_of_records)
    
