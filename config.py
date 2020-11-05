#! /usr/bin/python3
# -*- coding:utf-8 -*-

import configparser

class Configuration:
    DEFAULT = { 'Logging':{ 'LogToFile':'False'
                            'LogFileName':'znak_def.log', 
                            'LogToConsole':'True', 
                            'LogLevel':'INFO', 
                            'AutoOpenConsoleWindow':'True'
                            }
        
        
                }
    
    def __init__( self, name ):
        self.cfg = configparser.ConfigParser()
        self.cfg.read( name )
    
    def get( self, section, item ):
        res = None
        if section in self.cfg:
            if item in self.cfg[section]:
                res = self.cfg[section][item]
        if res == None:
            res = self.DEFAULT[section][item]
        return res
