#! /usr/bin/python3
# -*- coding:utf-8 -*-

import configparser


class Configuration:
    DEFAULT = {'Logging': {'LogToFile': 'False',
                           'LogFileName': 'znak_def.log',
                           'LogToConsole': 'True',
                           'LogLevel': 'INFO',
                           'AutoOpenConsoleWindow': 'False'
                           },
               'Database': {'Format': 'QSQLITE',
                            'DatabaseName': 'main.db'
                            }
               }
    
    def __init__(self, name):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(name)
    
    def get(self, section, item):
        res = None
        if section in self.cfg:
            if item in self.cfg[section]:
                res = self.cfg[section][item]
        if res is None:
            res = self.DEFAULT[section][item]
        return res


if __name__ == "__main__":
    print("Этот модуль является частью приложения.")
    print("Для запуска приложения выполните main.py")
