#!/usr/bin/python3
# -*- codingtype=utf-8-*-

import config
import log
import database
import ch_znak_api
from PyQt5 import QtWidgets
import main_window

CONFIG_FILE_NAME = "znak.ini"

if __name__ == "__main__":
    import sys
    cfg = config.Configuration(CONFIG_FILE_NAME)
    log = log.Log(cfg)
    db = database.Database(log, cfg)
    api = ch_znak_api.Ch_Znak_Api(log, cfg)
    api.do( 'get_question', {'filename':'out.txt' })
    api.do( 'certification', { 'input':'out.txt', 'output':'ecp.txt' } )
    api.do( 'get_token', {'filename':'ecp.txt'} )
    log.info("Создание главного окна.")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = main_window.MainWindow(log, cfg, db, api)
    mainWindow.show()
    sys.exit(app.exec_())
