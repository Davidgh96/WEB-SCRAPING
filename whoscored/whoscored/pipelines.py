# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import csv
import json
import mysql.connector
class WhoscoredPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_items.html' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['EquipoLocal', 'EquipoVisitante', 'Resultado', 'Comienzo', 'Fecha']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('datos.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class MySqlPipeline(object):
    """docstring for MySqlPipeline"""
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn= mysql.connector.connect(
            host ='localhost',
            user ='root',
            passwd ='',
            database ='fullleague'
        )
        self.curr=self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS fullleague_table""")
        self.curr.execute(""" create table fullleague_table(
                                id int auto_increment,
                                Fecha text,
                                Comienzo text,
                                Resultado text,
                                EquipoLocal text,
                                EquipoVisitante text,
                                EntrenadorLocal text,
                                EntrenadorVisitante text,
                                GoleadoresLocal text,
                                GoleadoresVisitante text,
                                FormacionLocal text,
                                FormacionVisitante text,
                                Estadio text,
                                Asistencia text,
                                Tiempo text,
                                Arbitro text,
                                PuntuacionLocal text,
                                PuntuacionVisitante text,
                                JugadoresTitularesLocal text,
                                JugadoresTitularesVisitante text,
                                SuplentesLocal text,
                                SuplentesVisitante text,
                                Cronologia text,
                                     primary key(id) )""" )

    def process_item(self,item,spider):
        self.store_database(item)
        return item

    def store_database(self,item):
      #  Cronologia_str=json.dumps(item['Cronologia'])
        self.curr.execute("""insert into fullleague_table (`Fecha`, `Comienzo`, `Resultado`, `EquipoLocal`,
            `EquipoVisitante`, `EntrenadorLocal`, `EntrenadorVisitante`, `GoleadoresLocal`,
            `GoleadoresVisitante`, `FormacionLocal`, `FormacionVisitante`, `Estadio`,`Asistencia`,
             `Tiempo`, `Arbitro`, `PuntuacionLocal`, `PuntuacionVisitante`,`JugadoresTitularesLocal`,
             `JugadoresTitularesVisitante`, `SuplentesLocal`,
             `SuplentesVisitante`,`Cronologia`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(
            item['Fecha'],
            item['Comienzo'],
            item['Resultado'],
            item['EquipoLocal'],
            item['EquipoVisitante'],
            item['EntrenadorLocal'],
            item['EntrenadorVisitante'],
            item['GoleadoresLocal'],
            item['GoleadoresVisitante'],
            item['FormacionLocal'],
            item['FormacionVisitante'],
            item['Estadio'],
            item['Asistencia'],
            item['Tiempo'],
            item['Arbitro'],
            item['PuntuacionLocal'],
            item['PuntuacionVisitante'],
            str(item['JugadoresTitularesLocal']),
            str(item['JugadoresTitularesVisitante']),
            str(item['SuplentesLocal']),
            str(item['SuplentesVisitante']),
            str(item['Cronologia'])
            ))

        self.conn.commit()