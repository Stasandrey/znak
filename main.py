#!/usr/bin/python3
# -*- codingtype=utf-8-*-

import config
import log
from PyQt5 import QtWidgets
import main_window

CONFIG_FILE_NAME = "znak.ini"

if __name__ == "__main__":
    import sys
    cfg = config.Configuration( CONFIG_FILE_NAME )
    log = log.Log( cfg )
    log.info( "Создание главного окна." )
    app = QtWidgets.QApplication( sys.argv )
    mainWindow = main_window.MainWindow()
    mainWindow.show()
    sys.exit( app.exec_() )
