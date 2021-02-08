from pymongo import MongoClient
import datetime


class Mongo_DB():

    def __init__(self, Mongo_URL = 'mongodb://localhost:27017/'):
        self.Client = MongoClient(Mongo_URL)

    def connect(self,DataBase = 'default', Collection = 'default'):
        self.DataBase = self.Client[DataBase]
        self.Collection = self.DataBase[Collection]

    def __insert(self, contents ):
        if type(contents) == list:
            self.Collection.insert_many(contents)
        elif type(contents) == dict:
            self.Collection.insert_one(contents)
        else:
            print("Data's format error !!!")

    
    def update(self, behavior = '' , spice = '', tags = ''):
        message = {}
        message['behavior'] = behavior
        message['spice'] = spice
        message['tags'] = tags
        message['date'] = datetime.datetime.utcnow()
        self.__insert(message)

Mongo = Mongo_DB()