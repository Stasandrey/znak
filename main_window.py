#! /usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import options_window
import console_window
import Ui_MainWindow

class MainWindow( QtWidgets.QMainWindow, Ui_MainWindow.Ui_MainWindow ):
    def __init__( self, parent = None):
        QtWidgets.QWidget.__init__( self, parent )
        self.setupUi( self )
        self.setCentralWidget( self.mdiArea )
        
        self.actConsole.triggered.connect( self.doConsole )
        self.actOptions.triggered.connect( self.doOptions )
        self.actExit.triggered.connect( self.close )
        
    def chooseSource( self ):
        pass

    def doConsole( self ):
        con = console_window.ConsoleWindow()
        self.mdiArea.addSubWindow( con )
        con.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        con.show()
#        self.console.show()

    def doOptions( self ):
        options = options_window.OptionsWindow()
        options.exec()

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
