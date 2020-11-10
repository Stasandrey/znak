#! /usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets, QtSql, QtCore
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
        self.stm.setTable( self.tbl_name )
        
        
        self.stm.setHeaderData( 0, QtCore.Qt.Horizontal, 'Модель' )
        self.stm.setHeaderData( 1, QtCore.Qt.Horizontal, 'Размер' )
        self.stm.setHeaderData( 2, QtCore.Qt.Horizontal, 'GTIN' )
        self.stm.setHeaderData( 3, QtCore.Qt.Horizontal, 'Сырье' )
        self.stm.setHeaderData( 4, QtCore.Qt.Horizontal, 'Количество' )
        
        
        self.stm.setRelation( 0, QtSql.QSqlRelation( "GTINS", 'GTIN', 'MODEL' ) )
        self.stm.setRelation( 1, QtSql.QSqlRelation( "GTINS", 'GTIN', 'SIZE' ) )
        
        self.stm.setSort( 3, QtCore.Qt.AscendingOrder )
        
        self.stm.select()
        self.table.setModel( self.stm )
        self.table.setColumnWidth( 2, 180 )
        
        self.list, self.models = self.readGtins()
        self.model.addItems( self.list )
        
        self.model.activated.connect( self.buildSizes )
        self.btnAdd.clicked.connect( self.add )
        self.btnDelete.clicked.connect( self.delete )
    
    def delete( self ):
        rec = self.stm.record( self.table.currentIndex().row() ) 
        print( rec.value( 2 ) )
        print( rec.value( 3 ) )
        print( rec.value( 4 ) )
        self.db.runSql( "DELETE FROM %s WHERE GTIN='%s' AND SOURCE='%s' AND NUMBER='%s';"%(
                          self.tbl_name, rec.value( 2 ), rec.value( 3 ), rec.value( 4 )  ) )  
        self.stm.select()
    
    def add( self ):
        if self.model.currentText() != '':
            if self.size.currentText() != '':
                if self.source.currentText() != '':
                    if self.count.value() > 0:
                        #rec = self.db.db.record( self.tbl_name )
                        #rec.setValue( 'NUMBER', self.count.value() )
                        #rec.setValue( 'SOURCE', self.source.currentText() )
                        res = self.db.runSql( "SELECT GTIN FROM GTINS WHERE MODEL = '%s' AND SIZE = '%s'"%(
                                                self.model.currentText(), self.size.currentText() ) )
                        print( res )
                        print( res[0]['GTIN'] )
                        #rec.setValue( 'GTIN', res[0]['GTIN'] )
                        #rec.setValue( 'MODEL', res[0]['GTIN'] )
                        #rec.setValue( 'SIZE', res[0]['GTIN'] )
                        #self.stm.insertRecord( -1, rec )
                        self.db.runSql( "INSERT INTO %s  VALUES ('%s','%s','%s','%s',%s);"%(
                                        self.tbl_name, res[0]['GTIN'], res[0]['GTIN'], res[0]['GTIN'], 
                                        self.source.currentText(), self.count.value() ) )
#                        
                        self.stm.select()
#    
    def buildSizes( self, text ):
        text = self.model.currentText()
        if text != '':
            self.size.clear()
            self.size.addItems( self.models[text] )
        #print( self.model.currentText() )
    
    def readGtins( self ):
        res = self.db.runSql( "SELECT * FROM GTINS;" )
        models = {}
        list = ['']
        for i in res:
            if i['MODEL'] in models:
               pass
            else:
                models.update( {i['MODEL']:[]} )
                list.append( i['MODEL'] )
            flag = False
            for k in models[i['MODEL']]:
                if k == i['SIZE']:
                    flag = True
            if flag == False:
                models[i['MODEL']].append( i['SIZE'] )
        return list, models    

    def resizeEvent( self, xy ):
        self.table.resize( xy.size().width() - 20, xy.size().height() - 60 )
        QtWidgets.QWidget.resizeEvent( self, xy )
        
if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )