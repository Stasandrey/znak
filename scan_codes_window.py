#! /usr/bin/python3
# -*- coding:utf-8 -*-
import fitz
import datetime
from barcode import EAN13
from barcode.writer import  ImageWriter
from wand.image import Image
from wand.drawing import Drawing

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
        self.page = None
        self.pdf = None
        self.img = None
        doc = fitz.open( name )
        text = ''
        for page in doc:
            # print( page.getImageList( full = True ) )
            text = text + page.getText()
        items = text.split( '\n' )
        flag = 0
        s = ''
        table = []
        for item in items:
            if flag == 1:
                s = s + item
                flag = 0
                table.append( s )
            if flag == 0:
                if item[0:4] == '0104':
                    s = item
                    flag = 1
        data = []
        for item in table:
            gtin = item[2:16]
            time = str( datetime.datetime.now() )
            filename = ''
            for q in time:
                if q == ':' or q == '-' or q == ' ' or q == '.':
                    filename = filename + '_'
                else:
                    filename = filename + q
            filename = gtin + '_' + filename
            code = { 'gtin':gtin, 'code':item, 'filename':filename }
            data.append( code )

        if self.img == None:
            self.page = 0
            self.pdf = name
            self.image = Image(filename='%s[%s]' % (self.pdf, self.page), resolution=300)
        for i, item in enumerate( data ):
            self.readImageNs( name, i, "images/%s"%( data[i]['filename'] ), data[i]['gtin'] )
        self.page = None
        self.pdf = None
        self.img = None
        for item in data:
            code = self.db.encode( item['code'] )
            self.db.runSql( "INSERT INTO CODES VALUES ( '%s', '%s', '%s', 'НС', '0' );"%(
                                item['gtin'],
                                code,
                                item['filename'] ) )

            print( item )
            print( self.db.decode( code ) )

# --------------------------------------------------------------------------------------------
    def readImageNs( self, name, i, filename, gtin ):
        koord = [[0, 415],
                 [420, 835],
                 [840, 1255],
                 [1260, 1675],
                 [1680, 2095],
                 [2105, 2520],
                 [2525, 2940],
                 [2945, 3360]]
        page = int(i / 8)
        n = i % 8
        print("Page %s" % (page))
        print("Image %s" % (n))

        print(gtin[1:14])
        with open('ean.png', 'wb') as f:
            EAN13('%s' % (gtin[1:13]), writer=ImageWriter()).write(f)

#        with  Image(filename='%s[%s]' % (name, page), resolution=300) as img:
        if page != self.page:
            self.image = Image(filename='%s[%s]' % (self.pdf, page), resolution=300)
            self.page = page

        with self.image.clone() as img:
            img.convert('png')
            img.crop(0, koord[n][0], 709, koord[n][1])
            draw = Drawing()
            ean = Image(filename="./ean.png", resolution=300).clone()
            draw.composite(operator="over", left=5, top=235, width=round(ean.width * 0.65),
                       height=round(ean.height * 0.65), image=ean)
            draw(img)
            img.save(filename='%s.png' % (filename))


# --------------------------------------------------------------------------------------------

    def scanDS( self, item ):
        pass

    def doChooseFiles( self ):
        res = QtWidgets.QFileDialog.getOpenFileNames( parent = self, caption = "Выбор файлов", 
                                                directory = QtCore.QDir.currentPath(), 
                                                filter = "pdf (*.pdf)" )
        if res[1] != '':
            self.fileNames = res[0]

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
