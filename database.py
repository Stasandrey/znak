#! /usr/bin/python3
# -*- coding:utf-8 -*-
import base64

from PyQt5 import QtSql


class Database:
    otgruzka = None
    
    def __init__(self, log, cfg):
        self.log = log
        self.cfg = cfg
        self.log.info("Конструктор Database ")
        format = cfg.get('Database', "Format")
        self.log.info("Формат базы данных %s" % (format))
        self.db = QtSql.QSqlDatabase.addDatabase(format)
        self.dbName = self.cfg.get('Database', 'DatabaseName')
        self.db.setDatabaseName(self.dbName)
        self.db.open()
        self.query = QtSql.QSqlQuery()
    
    def getTables(self):
        return self.db.tables()
    
    def createDatabase( self, name ):
        self.log.info( "Создание базы данных %s"%( name ) )
        self.db.close()
        self.db.setDatabaseName( name )
        self.dbName = name
        self.db.open()
        ## con.tables
        
        self.query = QtSql.QSqlQuery()
        self.runSql( "CREATE TABLE GTINS ( GTIN TEXT, MODEL TEXT, SIZE TEXT );" )     
        self.runSql( "CREATE TABLE OTGRUZKI ( NAME TEXT, TABLE_NAME TEXT )" )
        self.runSql( "CREATE TABLE CODES ( GTIN TEXT, CODE TEXT, FILENAME TEXT, SOURCE TEXT,STATE TEXT );" )
        #print( res )
        
        
    def changeDatabase( self, name ):
        self.log.info( "Открытие базы данных %s"%( name ) )
    
    def runSql( self, sql ):
        #self.log.info( "Выполнение SQL запроса %s"%( sql ) )
        res = self.query.exec( sql )
        res = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                item = {}
                for i in range( self.query.record().count() ):
                    item.update( { self.query.record().fieldName( i ): self.query.value( i ) } )
                res.append( item )
                self.query.next()
        self.query.finish()
        return res
    def encode( self, s ):
        return     base64.b64encode( s.encode( "UTF-8" ) ).decode( "UTF-8" )

    def decode( self, s ):
        return     base64.b64decode( s.encode( "UTF-8" ) ).decode( "UTF-8" )

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
