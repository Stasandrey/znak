#! /usr/bin/python3
# -*- coding:utf-8 -*-
import logging


class Log:
    LEVELS = {'DEBUG': logging.DEBUG,
              'INFO': logging.INFO,
              'WARNING': logging.WARNING,
              'ERROR': logging.ERROR,
              'CRITICAL': logging.CRITICAL
              }
    consoleWindow = None
    consoleLevel = 0

    def __init__(self, cfg):
        self.cfg = cfg
        fname = None
        if self.cfg.get('Logging', 'LogToFile') == "True":
            fname = self.cfg.get('Logging', 'LogFileName')
            open(fname, 'wt').close()
        level = self.LEVELS[self.cfg.get('Logging', 'LogLevel')]
        self.log = logging.basicConfig(filename=fname, level=level)
        self.logToConsole = False
        if self.cfg.get('Logging', 'LogToConsole') == 'True':
            self.logToConsole = True
    
    def debug(self, s):
        logging.debug(s)
        if self.logToConsole:
            print("DEBUG:%s" % (s))
        if self.consoleWindow is not None:
            if self.consoleLevel <= 3:
                self.consoleWindow.widget().text.insertPlainText('DEBUG:%s\n' % (s))
                self.consoleWindow.repaint()
    
    def info(self, s):
        logging.info(s)
        if self.logToConsole:
            print("INFO:%s" % (s))
        if self.consoleWindow is not None:
            if self.consoleLevel <= 4:
                self.consoleWindow.widget().text.insertPlainText('INFO:%s\n' % (s))
                # self.consoleWindow.text.insertPlainText( 'INFO:%s\n'%( s ) )
                self.consoleWindow.repaint()
            
    def warning(self, s):
        logging.warning(s)
        if self.logToConsole:
            print("WARNING:%s" % (s))
        if self.consoleWindow is not None:
            if self.consoleLevel <= 2:
                self.consoleWindow.widget().text.insertPlainText('WARNING:%s\n' % (s))
                # self.consoleWindow.text.insertPlainText( 'WARNING:%s\n'%( s ) )
                self.consoleWindow.repaint()
            
    def error(self, s):
        logging.error(s)
        if self.logToConsole:
            print("ERROR:%s" % (s))
        if self.consoleWindow is not None:
            if self.consoleLevel <= 2:
                self.consoleWindow.widget().text.insertPlainText('ERROR:%s\n' % (s))
                # self.consoleWindow.text.insertPlainText( 'ERROR:%s\n'%( s ) )
                self.consoleWindow.repaint()
            

if __name__ == "__main__":
    print("Этот модуль является частью приложения.")
    print("Для запуска приложения выполните main.py")
