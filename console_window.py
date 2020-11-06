#! /usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import Ui_ConsoleWindow

class ConsoleWindow( QtWidgets.QDialog, Ui_ConsoleWindow.Ui_ConsoleWindow ):
    def __init__( self, parent = None):
        QtWidgets.QWidget.__init__( self, parent )
        self.setupUi( self )
       

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
