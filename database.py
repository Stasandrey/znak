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
        
    def createDatabase( self, name ):
        self.log.info( "Создание базы данных %s"%( name ) )
        self.db.setDatabaseName( name )
        self.db.open()
        
    def changeDatabase( self, name ):
        self.log.info( "Открытие базы данных %s"%( name ) )
    
if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
