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
        if self.cfg( 'Logging', 'LoggingToFile' ) == "True":
            fname = self.cfg( 'Logging', 'LogFileName' )
        level = self.LEVELS[self.cfg( 'Logging', 'LogLevel' )]
        self.log = logging.basicConfig( filename = fname, encoding = 'utf-8', level=level )
    
    def debug( self, s ):
        logging.debug( s )
        
    def info( self, s ):
        logging.info( s )
        
    def warning( self, s ):
       logging.warning( s )
      
    def error( self, s ): 
       logging.error( s ) 

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
