#! /usr/bin/python3
# -*- coding:utf-8 -*-
import fitz

from PyQt5 import QtWidgets, QtCore
import Ui_ScanCodesWindow

class ScanCodesWindow( QtWidgets.QMainWindow, Ui_ScanCodesWindow.Ui_ScanCodesWindow ):
    files = ''
    
    def __init__( self, log, cfg, db, api, parent = None):
        self.log = log
        self.cfg = cfg
        self.db = db
        self.api = api
        self.log.info( "Конструктор окна сканирования кодов" )
        QtWidgets.QWidget.__init__( self, parent )
        self.setupUi( self )
        self.chooseFiles.clicked.connect( self.doChooseFiles )
        self.scan.clicked.connect( self.doScanCodes )

    def doScanCodes( self ):
        if self.fileNames != '':
            if self.source.currentText() != '':
                for item in self.fileNames:
                    if self.source.currentText() == 'НС':
                        self.scanNS( item )
                    elif self.source.currentText() == 'ДС':
                        self.scanDS( item )
                
    def scanNS( self, name ):
        doc = fitz.open( name )
        for page in doc:
            print( page.getImageList( full = True ) )
            print( page.getText() )

    def doChooseFiles( self ):
        res = QtWidgets.QFileDialog.getOpenFileNames( parent = self, caption = "Выбор файлов", 
                                                directory = QtCore.QDir.currentPath(), 
                                                filter = "pdf (*.pdf)" )
        if res[1] != '':
            self.fileNames = res[0]

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
