import json
import codecs   
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import os,shutil
from scrapy.contrib.exporter import JsonLinesItemExporter,ScrapyJSONEncoder
from MovieRecommendation import myConfig
 

class JsonItemExporter(JsonLinesItemExporter):

    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file
        self.encoder = ScrapyJSONEncoder(**kwargs)
        self.first_item = True

    def start_exporting(self):
        self.file.write("[")

    def finish_exporting(self):
        self.file.write("]")

    def export_item(self, item):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(',\n')
#        itemdict = dict(self._get_serialized_fields(item))
        line = json.dumps(dict(item),ensure_ascii=False)
        self.file.write(line)


class JsonExportPipeline(object):
    filePattern_final = 'json.final'
    filePattern_processing = 'json.processing'
    fileCount = 0
    recordCount = 0
    filePath = myConfig.fileTempPath

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}
        

    def fileCleanUp(self):
        for filename in os.listdir('.'):
             if(filename.endswith(self.filePattern_final) or filename.endswith(self.filePattern_processing)):
                os.remove(filename)
        

    def spider_opened(self, spider):
        self.fileCleanUp()
        file = codecs.open('%s_items.json.processing' % self.fileCount, 'w+b',encoding='utf-8')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        os.rename('%s_items.json.processing' % self.fileCount, '%s_items.json.final' % self.fileCount)
        shutil.move('./%s_items.json.final' % self.fileCount ,self.filePath+'/%s_items.json.final' % self.fileCount )   
        
    def spider_closed_cur(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()     
        

    def process_item(self, item, spider):
#        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        if(self.recordCount<100):
            self.exporter.export_item(item)
            self.recordCount = self.recordCount + 1
        else:
            self.recordCount = 0
            self.spider_closed_cur(spider)
            os.rename('%s_items.json.processing' % self.fileCount, '%s_items.json.final' % self.fileCount)
            shutil.move('./%s_items.json.final' % self.fileCount ,self.filePath+'%s_items.json.final' % self.fileCount )   
            self.fileCount = self.fileCount + 1
            self.spider_opened(spider)
        return item