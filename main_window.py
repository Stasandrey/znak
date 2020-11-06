#! /usr/bin/python3
# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets
import Ui_MainWindow

class MainWindow( QtWidgets.QMainWindow, Ui_MainWindow.Ui_MainWindow ):
    def __init__( self, parent = None):
        QtWidgets.QWidget.__init__( self, parent )
        self.setupUi( self )
        self.setCentralWidget( self.mdiArea )
        
        self.actOptions.triggered.connect( self.doOptions )
        self.actExit.triggered.connect( self.close )
        
    def chooseSource( self ):
        pass

    def doOptions( self ):
        pass

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
