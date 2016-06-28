'''
Created on 2015-5-18

@author: darcyyang
'''
import json,datetime
import os,shutil
import codecs   
from MovieRecommendation.helper.doc_dao import DAO
from MovieRecommendation.helper.version_dao import VersionDAO

class DataLoader():
    
    filePattern_processing = 'json.processing'
    filePattern_final = 'json.final'

    DATA_FILE_PATH = './crapyTemp'
    dao = None
    version_dao = None
    version = 1
    
    newRecord = 0
    updatedRecord = 0
    
    def __init__(self):
        
       print 'start Loader'
       self.dao = DAO()
       self.version_dao = VersionDAO()
       self.initVersion()
       
    def initVersion(self):
        item = self.loadCurrentVersion()
        if(item):
            self.version = item['version'] + 1
#            self.version_dao.insertData(item)
#        else:
#            
#         new_posts = [{"author": "Mike",
#              "text": "Another post!",
#               "tags": ["bulk", "insert"],
#               "date": datetime.datetime(2009, 11, 12, 11, 14)},
#              {"author": "Eliot",
#               "title": "MongoDB is fun",
#               "text": "and pretty easy too!",
#               "date": datetime.datetime(2009, 11, 10, 10, 45)}]
        
        
    def version_pack(self):
        print ('current version ', self.version)
        print ('Totally Insert Records: ' , self.newRecord)
        print ('Totally Updated Records: ' , self.updatedRecord)    
        print ('Date',datetime.datetime.now() )
        new_version = {"version": self.version,
                        "inserted_record": self.newRecord,
                        "updated_record":self.updatedRecord,
                        "date": datetime.datetime.now(),
                        "link": datetime.datetime.now()}
        
        self.version_dao.insertData(new_version)

    def loadCurrentVersion(self):
        return self.version_dao.getLatestItem()
        
            
    def retrieveFiles(self):
        for filename in os.listdir(self.DATA_FILE_PATH):
            if(filename.endswith(self.filePattern_final)):
                print 'Start loading data from ' +filename
                self.loadData(self.DATA_FILE_PATH + '/' +filename)
        self.version_pack()
        self.fileCleanUp()
                
    def loadData(self,filename):
        file = codecs.open(filename, 'r', encoding='utf-8',buffering=1)

        content =  file.read()
#        dic_content = dict(content)
        test = json.loads(content, encoding='utf-8')
        for jsonLineItem in test:
         result = self.dao.findDataByKeyValue('name', jsonLineItem['name'])
         jsonLineItem['version'] = self.version
         if(not result):
           self.dao.insertData(jsonLineItem)
           self.newRecord = self.newRecord + 1
         else:
           result_ver = -1  
           if 'version' in result:
               result_ver = result['version'] 
           if(result_ver != self.version):
              self.dao.replaceRowData(result,jsonLineItem)
              self.updatedRecord = self.updatedRecord + 1
        print('Finish Data Load from ' + filename)
           
    def fileCleanUp(self):
        for filename in os.listdir(self.DATA_FILE_PATH):
             if(filename.endswith(self.filePattern_final)):
                print 'Remove file ' + filename
                os.remove(self.DATA_FILE_PATH + '/' + filename)
        
DataLoader().retrieveFiles()
        
        
        
        
        
        
                  
                
        