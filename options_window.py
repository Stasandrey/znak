#! /usr/bin/python3
# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets
import Ui_OptionsWindow

class OptionsWindow( QtWidgets.QDialog, Ui_OptionsWindow.Ui_OptionsWindow ):
    def __init__( self, parent = None):
        QtWidgets.QWidget.__init__( self, parent )
        self.setupUi( self )
       

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
