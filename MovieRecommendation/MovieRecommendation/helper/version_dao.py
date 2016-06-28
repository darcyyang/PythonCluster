'''
Created on 2015-5-15

@author: darcyyang
'''
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
class VersionDAO:
    
    DBIP = 'localhost'
    DB_PORT = 27017

    dbInstance = None
    document = None
    
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.dbInstance = client['douban']
        self.document = self.dbInstance['movie']
        self.document.create_index([('link',1)],unique=True)

    def insertMulData(self,obj):
        ids = self.document.insert_many(obj)
        return ids
    
    def insertData(self,item):
        post_id = self.document.insert_one(item).inserted_id
        print('Add ' , post_id)
    
    def replaceRowData(self,pre_item,item):
        self.document.find_one_and_replace(pre_item,item)
        print('Update ' , pre_item['_id'])
#    def isExists(self,key,value):
#        self.document.
        
    def getLatestItem(self):
        return self.document.find_one()
        
        
        
        