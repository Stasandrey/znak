#! /usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import random
#import options_window
import console_window
import otgruzka_window
import scan_codes_window

import Ui_MainWindow

class MainWindow( QtWidgets.QMainWindow, Ui_MainWindow.Ui_MainWindow ):
    console = None
    isConsole = False
    def __init__( self, log, cfg, db, api, parent = None):
        self.log = log
        self.cfg = cfg
        self.db = db
        self.api = api
        self.log.info( "Конструктор главного окна" )
        QtWidgets.QWidget.__init__( self, parent )
        self.setupUi( self )
        self.setCentralWidget( self.mdiArea )
        self.log.info( "Создание окна консоли" )  
        self.console = console_window.ConsoleWindow( log, cfg )
        self.console.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        self.log.consoleWindow = self.console
        if self.cfg.get( 'Logging', 'AutoOpenConsoleWindow' ) == 'True':
            self.isConsole = True
            self.mdiArea.addSubWindow( self.console )
            self.console.show()
        self.actCreateDatabase.triggered.connect( self.doCreateDatabase )
        self.actChangeDatabase.triggered.connect( self.doChangeDatabase )
        self.actSyncDatabase.triggered.connect( self.doSyncDatabase )
        self.actConsole.triggered.connect( self.doConsole )
        self.actOptions.triggered.connect( self.doOptions )
        self.actExit.triggered.connect( self.close )
        self.actNewOtgruzka.triggered.connect( self.doNewOtgruzka )
        self.actChangeOtgruzka.triggered.connect( self.doChangeOtgruzka )
        self.actScanCodes.triggered.connect( self.doScanCodes )
    
    def doScanCodes( self ):
        self.scanCodes = scan_codes_window.ScanCodesWindow( self.log, self.cfg,
                                                       self.db, self.api )
        self.scanCodes.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        self.mdiArea.addSubWindow( self.scanCodes )
        self.scanCodes.resize( 400, 400 )
        self.scanCodes.show()
    
    def doNewOtgruzka( self ):
        s, ok = QtWidgets.QInputDialog.getText( self, "Новая отгрузка", 
                                            "Введите название отгрузки" )
        if ok:
            tblName = "TBL_" + str( random.randrange( 1000000, 9999999 ) )
            while len( self.db.runSql( "SELECT * FROM OTGRUZKI WHERE TBL_NAME = '%s';"%(
                          tblName ) ) ) > 0:
                tblName = str( random.randrange( 1000000, 9999999 ) )
            self.db.runSql( "INSERT INTO OTGRUZKI VALUES ( '%s', '%s' );"%(
                          s, tblName) )
            self.db.runSql( "CREATE TABLE %s ( MODEL TEXT, SIZE TEXT, GTIN TEXT, SOURCE TEXT, NUMBER INTEGER );"%( tblName ) )
            print( "CREATE TABLE %s ( GTIN TEXT, SOURCE TEXT, NUMBER INTEGER );"%( tblName ) )
            self.log.info( 'Создание отгрузки %s TBL_NAME = %s'%( s, tblName ) )
            self.db.otgruska = tblName
            self.doChangeOtgruzka( tblName )
    
    def doChangeOtgruzka( self, name = '' ):
        list = [] 
        res = self.db.runSql( "SELECT * FROM OTGRUZKI;" )
        for item in res:
            list.append( item['NAME'] )
        if name == False:
            s, ok = QtWidgets.QInputDialog.getItem( self, "Смена отгрузки", 
                                                    "Выберите отгрузку", 
                                                    list, 
                                                    current = 0)
            if ok:
                name = s
        if name != '':
            if name != False:
                for i in res:
                    if name == i['NAME']:
                        tbl = i['TABLE_NAME']
                self.otgruzka = otgruzka_window.OtgruzkaWindow( self.log, self.cfg,
                                                                self.db, self.api, 
                                                                tbl, name )
                self.otgruzka.setAttribute( QtCore.Qt.WA_DeleteOnClose )
                self.mdiArea.addSubWindow( self.otgruzka )
                self.otgruzka.resize( 400, 400 )
                self.otgruzka.show()
    
    def doCreateDatabase( self ):
        res = QtWidgets.QFileDialog.getSaveFileName( caption = "Выберите имя и место хранения базы данных.", 
                               directory = QtCore.QDir.currentPath(), 
                               filter = "All (*)")
        if res[0] != "":
            self.log.info( "Создание новой базы данных%s"%( res[0] ) )
            self.db.createDatabase( res[0] )
        
    def doChangeDatabase( self ):
        pass

    def doSyncDatabase( self ):
        self.log.info( "Синхронизация базы данных с системой Честный знак" )
        res = ( self.api.do( 'get_gtins', {} ) )['data']['results']
        n = 0
        gtin = []
        for i in res:
            mr = ['','']
            if 'model' in i:
                if 'productSize' in i:
                    if 'gtin' in i:    
                        mr = []
                        mr.append( i['gtin'] )
                        mr.append( i['model'][i['model'].find( 'Модель' ) + 7:len( i['model'] )] )
                        mr.append( i['productSize'] )
                        gtin.append( mr )
                        n = n + 1
        self.log.info( 'Получено %s кодов.'%( n ) )
        self.log.info( "Удаление записей" )
        self.db.runSql( "DELETE FROM GTINS;" )
        self.log.info( "Запись в базуданных" )
        n = 0
        for item in gtin:
            self.db.runSql( "INSERT INTO GTINS VALUES ( '%s', '%s', '%s' );"%(
                                item[0], item[1], item[2] ) )
            n = n + 1
            print( n )
        self.log.info( 'OK' )

    def doConsole( self ):
        self.log.info( "Показать консоль" )
        if self.isConsole ==False:
            self.isConsole = True
            self.mdiArea.addSubWindow( self.console )
            self.console.show()
        else:
            self.isConsole = False
            self.console.hide()
            self.mdiArea.removeSubWindow( self.console )
 
    def doOptions( self ):
        self.log.warning( "Показать Настройки" )
        #options = options_window.OptionsWindow()
        #options.exec()

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
