#! /usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtSql
import Ui_OtgruzkaWindow

class OtgruzkaWindow( QtWidgets.QWidget, Ui_OtgruzkaWindow.Ui_OtgruzkaWindow ):
    console = None
    isConsole = False
    def __init__( self, log, cfg, db, api, tbl_name, name, parent = None):
        self.log = log
        self.cfg = cfg
        self.db = db
        self.api = api
        self.tbl_name = tbl_name
        self.o_name = name
        self.log.info( "Конструктор окна отгрузки" )
        QtWidgets.QWidget.__init__( self, parent )
        self.setupUi( self )
        self.stm = QtSql.QSqlRelationalTableModel( self )
        print( tbl_name )
        self.stm.setTable( self.tbl_name )
        self.stm.setRelation( 0, QtSql.QSqlRelation( "GTINS", 'GTIN', 'MODEL' ) )
        self.stm.setRelation( 1, QtSql.QSqlRelation( "GTINS", 'GTIN', 'SIZE' ) )
        
        self.stm.select()
        self.table.setModel( self.stm )
        

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
