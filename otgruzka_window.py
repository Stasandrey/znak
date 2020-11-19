#! /usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets, QtSql, QtCore, QtGui, QtPrintSupport
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
        self.printer = QtPrintSupport.QPrinter()
        self.printer.setResolution( 203 )

        self.stm = QtSql.QSqlRelationalTableModel( self )
        self.stm.setTable( self.tbl_name )

        self.stm.setHeaderData( 0, QtCore.Qt.Horizontal, 'Модель' )
        self.stm.setHeaderData( 1, QtCore.Qt.Horizontal, 'Размер' )
        self.stm.setHeaderData( 2, QtCore.Qt.Horizontal, 'GTIN' )
        self.stm.setHeaderData( 3, QtCore.Qt.Horizontal, 'Сырье' )
        self.stm.setHeaderData( 4, QtCore.Qt.Horizontal, 'Количество' )
        self.stm.setHeaderData( 5, QtCore.Qt.Horizontal, 'Напечатано' )
        self.stm.setHeaderData( 6, QtCore.Qt.Horizontal, 'Доступно' )

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
        self.prn.clicked.connect( self.doPrn )

    def doPrn( self ):
        rec = self.stm.record(self.table.currentIndex().row())
        if rec.value( 4 ) >= rec.value( 6 ):
            maximum = rec.value( 6 )
            now = rec.value( 6 )
        else:
            maximum = rec.value( 4 )
            now = rec.value( 4 )
        n, ok = QtWidgets.QInputDialog.getInt( self, 'Печать кодов идентефикации',
                                               'Модель %s размер %s. Максимум %s.'%(
                                                rec.value( 0 ), rec.value( 1 ), maximum ),
                                               value = now, min = 1, max = maximum)
        if ok:
            res = self.db.runSql( "SELECT * FROM CODES WHERE GTIN = '%s' AND STATE = '0' AND SOURCE = '%s';"%(
                                   rec.value( 2 ), rec.value( 3 ) ) )
            now = n
            printed = []
            for item in enumerate( res ):
                if item[0] < now:
                    printed.append( item[1] )
            print( printed )
            setup = QtPrintSupport.QPrintDialog( self.printer, self )
            setup.setOption( QtPrintSupport.QAbstractPrintDialog.PrintToFile,
                             on = False )
            setup.setOption( QtPrintSupport.QAbstractPrintDialog.PrintPageRange,
                             on = False )
            setup.setOption( QtPrintSupport.QAbstractPrintDialog.PrintCollateCopies,
                             on = False )
            setup.setOption( QtPrintSupport.QAbstractPrintDialog.PrintCurrentPage,
                             on = False )
            setup.exec()

            painter = QtGui.QPainter()
            painter.begin( self.printer )

            for item in enumerate( printed ):
                print( item )

                pixmap = QtGui.QPixmap( "images/%s.png" % (item[1]['FILENAME']) )
                pixmap = pixmap.scaled( self.printer.width(),
                                        self.printer.height(),
                                        aspectRatioMode = QtCore.Qt.KeepAspectRatio )
                painter.drawPixmap( 0, 0, pixmap )
                self.db.runSql( "UPDATE CODES SET STATE = '%s' WHERE CODE = '%s';"%(
                                            self.tbl_name,item[1]['CODE']  ) )
                #self.db.runSql( "UPDATE CODES SET PRINTED = %s WHERE " )
                if item[0] < now - 1:
                    self.printer.newPage()
            painter.end()





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

                        result = self.db.runSql( "SELECT * FROM CODES WHERE GTIN = '%s' AND SOURCE = '%s' AND STATE = '0';"%(
                                                res[0]['GTIN'], self.source.currentText() ) )
                        print( 'Available' )
                        print( result )
                        n = len( result )
                        self.db.runSql( "INSERT INTO %s  VALUES ('%s','%s','%s','%s',%s, 0, %s);"%(
                                        self.tbl_name, res[0]['GTIN'], res[0]['GTIN'], res[0]['GTIN'], 
                                        self.source.currentText(), self.count.value(), n ) )
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
