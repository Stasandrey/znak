#! /usr/bin/python3
# -*- coding:utf-8 -*-
from PyQt5 import QtSql
class Database:
    
    def __init__( self, log, cfg ):
        self.log = log
        self.cfg = cfg
        self.log.info( "Конструктор Database " )
        format = cfg.get( 'Database', "Format" )
        self.log.info( "Формат базы данных %s"%( format ) )
        self.db = QtSql.QSqlDatabase.addDatabase( format )
        self.dbName = self.cfg.get( 'Database', 'DatabaseName' )
        self.db.setDatabaseName( self.dbName )
        self.db.open()
        self.query = QtSql.QSqlQuery()
        
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
        #print( res )
        
        
    def changeDatabase( self, name ):
        self.log.info( "Открытие базы данных %s"%( name ) )
    
    def runSql( self, sql ):
        #self.log.info( "Выполнение SQL запроса %s"%( sql ) )
        self.query.exec( sql )
        self.query.finish()
    
if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
