#! /usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5 import QtCore, QtWidgets

#import options_window
import console_window
import Ui_MainWindow

class MainWindow( QtWidgets.QMainWindow, Ui_MainWindow.Ui_MainWindow ):
    console = None
    isConsole = False
    def __init__( self, log, cfg, db, parent = None):
        self.log = log
        self.cfg = cfg
        self.db = db
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
        
        self.actCreateDatabase.triggered.connect( self.createDatabase )
        self.actChangeDatabase.triggered.connect( self.changeDatabase )
        self.actConsole.triggered.connect( self.doConsole )
        self.actOptions.triggered.connect( self.doOptions )
        self.actExit.triggered.connect( self.close )
        
    def createDatabase( self ):
        res = QtWidgets.QFileDialog.getSaveFileName( caption = "Выберите имя и место хранения базы данных.", 
                               directory = QtCore.QDir.currentPath(), 
                               filter = "All (*)")
        if res[0] != "":
            self.db.createDatabase( res[0] )
        
    def changeDatabase( self ):
        pass

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
