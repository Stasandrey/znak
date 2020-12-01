#! /usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import Ui_ConsoleWindow


class ConsoleWindow(QtWidgets.QWidget, Ui_ConsoleWindow.Ui_ConsoleWindow):

    def __init__(self, log, cfg, parent=None):
        self.log = log
        self.cfg = cfg
        self.log.info("Конструктор окна консоли")
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.resize(300, 200)
    
        self.level.currentIndexChanged.connect(self.changeLevel)

    def changeLevel(self, text):
        level = 4 - text
        self.log.info("Изменение уровня отладки консоли на %s" % (level))
        self.log.consoleLevel = level
    
    def resizeEvent(self, xy):
        self.text.resize(xy.size().width() - 20, xy.size().height() - 60)
        QtWidgets.QWidget.resizeEvent(self, xy)


if __name__ == "__main__":
    print("Этот модуль является частью приложения.")
    print("Для запуска приложения выполните main.py")
