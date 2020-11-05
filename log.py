#! /usr/bin/python3
# -*- coding:utf-8 -*-
import logging

class Log:
    LEVELS = {  'DEBUG':logging.DEBUG, 
                'INFO':logging.INFO, 
                'WARNING':logging.WARNING, 
                'ERROR':logging.ERROR, 
                'CRITICAL':logging.CRITICAL        
                }
    
    def __init__( self, cfg ):
        self.cfg = cfg
        fname = None
        if self.cfg.get( 'Logging', 'LogToFile' ) == "True":
            fname = self.cfg.get( 'Logging', 'LogFileName' )
            open( fname, 'wt' ).close()
        level = self.LEVELS[self.cfg.get( 'Logging', 'LogLevel' )]
        self.log = logging.basicConfig( filename = fname, level=level )
        self.logToConsole = False
        if self.cfg.get( 'Logging', 'LogToConsole' ) == 'True':
            self.logToConsole = True
    
    def debug( self, s ):
        logging.debug( s )
        if self.logToConsole:
            print( s )
    
    def info( self, s ):
        logging.info( s )
        if self.logToConsole:
            print( s )
            
    def warning( self, s ):
        logging.warning( s )
        if self.logToConsole:
            print( s )
            
    def error( self, s ): 
        logging.error( s ) 
        if self.logToConsole:
            print( s )
            
if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
