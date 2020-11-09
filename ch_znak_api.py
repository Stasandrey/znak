#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import requests
import os
#import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9kdWN0X2dyb3VwX2luZm8iOlt7Im5hbWUiOiJzaG9lcyIsInN0YXR1cyI6IjUiLCJ0eXBlcyI6WyJQUk9EVUNFUiIsIklNUE9SVEVSIiwiVFJBREVfUEFSVElDSVBBTlQiLCJXSE9MRVNBTEVSIl19LHsibmFtZSI6ImxwIiwic3RhdHVzIjoiNSIsInR5cGVzIjpbIlBST0RVQ0VSIiwiSU1QT1JURVIiLCJUUkFERV9QQVJUSUNJUEFOVCIsIldIT0xFU0FMRVIiXX1dLCJ1c2VyX3N0YXR1cyI6IkFDVElWRSIsInVzZXJfbmFtZSI6bnVsbCwiaW5uIjoiNzcxOTgwODA2MSIsInBpZCI6NjAwMDE1MjE5LCJhdXRob3JpdGllcyI6WyJDUlBULUtNLU9SREVSUy5FTUlTU0lPTi1SRUdJU1RSQVItRkFDQURFLUNPTlRST0xMRVIuUkVBRElORy5SRUFEIiwiQ1JQVC1GQUNBREUuUFJPRklMRS1DT05UUk9MTEVSLkNPTVBBTlkuUkVBRCIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLkFHR1JFR0FUSU9OLkNSRUFURSIsIkNSUFQtS00tT1JERVJTLk9SREVSLUZBQ0FERS1DT05UUk9MTEVSLk1PRElGWUlORy5XUklURSIsIkNSUFQtS00tT1JERVJTLlBBUlRJQ0lQQU5ULldSSVRFIiwiQ1JQVC1LTS1PUkRFUlMuUEFSVElDSVBBTlQtT1ItT1BFUkFUT1IuV1JJVEUiLCJDUlBULUtNLU9SREVSUy5PUkRFUi1GQUNBREUtQ09OVFJPTExFUi5PUkRFUlMtRlJPTS1TVVouQ1JFQVRFIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuU0hJUE1FTlQuQ1JFQVRFIiwiQ1JQVC1MSy1ET0MtQVBJLkFQUC1VU0VSLUNPTlRST0xMRVIuREVMRVRFIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuQ09NTUlTU0lPTklORy5SRUFEIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuUkVBR0dSRUdBVElPTi5DUkVBVEUiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5MUF9SRVRVUk4uUkVBRCIsIkNSUFQtS00tT1JERVJTLk9SREVSLUZBQ0FERS1DT05UUk9MTEVSLkNSRUFUSU5HLURSQUZULkNSRUFURSIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLlJFTUFSS0lORy5DUkVBVEUiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5ESVNBR0dSRUdBVElPTi5SRUFEIiwiQ1JQVC1LTS1PUkRFUlMuTEFCRUwtVEVNUExBVEUtRkFDQURFLUNPTlRST0xMRVIuVVBEQVRJTkcuV1JJVEUiLCJST0xFX09SR19JTVBPUlRFUiIsIkNSUFQtS00tT1JERVJTLk9SREVSLUZBQ0FERS1DT05UUk9MTEVSLkNSRUFUSU5HLkNSRUFURSIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLkNST1NTQk9SREVSLkNSRUFURSIsIkNSUFQtTEstRE9DLUFQSS5BREQtQ0VSVC1DT05UUk9MTEVSLkNSRUFURSIsIlJPTEVfVVNFUiIsIkVMSy1QUk9GSUxFLlJFQUQiLCJDUlBULUtNLU9SREVSUy5TVVotUkVHSVNUUlktRkFDQURFLUNPTlRST0xMRVIuQ1JFQVRJTkcuQ1JFQVRFIiwiUk9MRV9PUkdfVFJBREVfUEFSVElDSVBBTlQiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5DT05UUkFDVC1DT01NSVNTSU9OSU5HLkNSRUFURSIsIkNSUFQtRkFDQURFLk1BUktFRC1QUk9EVUNUUy1DT05UUk9MTEVSLlJFQUQiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5BR0dSRUdBVElPTi5SRUFEIiwiSU5OXzc3MTk4MDgwNjEiLCJDUlBULUZBQ0FERS5BUFAtVVNFUi1DT05UUk9MTEVSLkxJU1QtUkVNT1ZFRC5SRUFEIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuQUNDRVBUQU5DRS5SRUFEIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuS00tQVBQTElFRC1DQU5DRUwuQ1JFQVRFIiwiUk9MRV9PUkdf0KPRh9Cw0YHRgtC90LjQuiDQvtCx0L7RgNC-0YLQsCIsIlJPTEVfT1JHX1dIT0xFU0FMRVIiLCJDUlBULUZBQ0FERS5DSVMtQ09OVFJPTExFUi5SRVBPUlQuRE9XTkxPQUQiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5MUF9JTlRST0RVQ0VfT1NULlJFQUQiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5DT01NSVNTSU9OSU5HLkNSRUFURSIsIkNSUFQtS00tT1JERVJTLkxBQkVMLVRFTVBMQVRFLUZBQ0FERS1DT05UUk9MTEVSLlJFQURJTkctREVGQVVMVFMtQlktU1VaLlJFQUQiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5ESVNBR0dSRUdBVElPTi5DUkVBVEUiLCJST0xFX1NVWiIsIkNSUFQtS00tT1JERVJTLkxBQkVMLVRFTVBMQVRFLUZBQ0FERS1DT05UUk9MTEVSLlJFQURJTkctQlktU1VaLlJFQUQiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5MT0FOLkNSRUFURSIsIkNSUFQtS00tT1JERVJTLkxBQkVMLVRFTVBMQVRFLUZBQ0FERS1DT05UUk9MTEVSLkNSRUFUSU5HLkNSRUFURSIsIkNSUFQtRkFDQURFLkFQUC1VU0VSLUNPTlRST0xMRVIuTElTVC1BQ1RJVkUuUkVBRCIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLlNISVBNRU5ULlJFQUQiLCJST0xFX09SR1_Qn9GA0L7QuNC30LLQvtC00LjRgtC10LvRjCIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLk9TVF9ERVNDUklQVElPTi5DUkVBVEUiLCJDUlBULUtNLU9SREVSUy5MQUJFTC1URU1QTEFURS1GQUNBREUtQ09OVFJPTExFUi5SRUFESU5HLlJFQUQiLCJDUlBULUtNLU9SREVSUy5TVVouV1JJVEUiLCJST0xFX09SR19QUk9EVUNFUiIsIkNSUFQtS00tT1JERVJTLk9SREVSLUZBQ0FERS1DT05UUk9MTEVSLlNVWi1FVkVOVFMuQ1JFQVRFIiwiQ1JQVC1LTS1PUkRFUlMuTEFCRUwtVEVNUExBVEUtRkFDQURFLUNPTlRST0xMRVIuRE9XTkxPQURJTkcuRE9XTkxPQUQiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5TSElQLUNST1NTQk9SREVSLkNSRUFURSIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLlJFQ0VJUFQuQ1JFQVRFIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuT1NUX0NPTVBMRVRFX0RFU0NSSVBUSU9OLkNSRUFURSIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLklNUE9SVC1DT01NSVNTSU9OSU5HLkNSRUFURSIsIlJPTEVfT1JHX9CY0LzQv9C-0YDRgtC10YAg0YLQvtCy0LDRgNCwIiwiRUxLLVJFR0lTVFJBVElPTi5XUklURSIsIkNSUFQtTEstRE9DLUFQSS5BUFAtVVNFUi1DT05UUk9MTEVSLkNSRUFURSIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLkxQX1JFVFVSTi5DUkVBVEUiLCJDUlBULUZBQ0FERS5QQVJUSUNJUEFOVC1DT05UUk9MTEVSLkdFVC1CWS1JTk4uUkVBRCIsIkNSUFQtTEstRE9DLUFQSS5EUkFGVC5BRE1JTklTVFJBVElPTiIsIkNSUFQtRkFDQURFLkNJUy1DT05UUk9MTEVSLlNFQVJDSC5SRUFEIiwiUk9MRV9PUkdf0J7Qv9GC0L7QstCw0Y8g0YLQvtGA0LPQvtCy0LvRjyIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLlJFQUdHUkVHQVRJT04uUkVBRCIsIkNSUFQtS00tT1JERVJTLlBBUlRJQ0lQQU5ULU9SLU9QRVJBVE9SLlJFQUQiLCJDUlBULUxLLURPQy1BUEkuUkVTVU1FLUFDQ0VTUy1DT05UUk9MTEVSLkNSRUFURSIsIkNSUFQtS00tT1JERVJTLlNVWi1SRUdJU1RSWS1GQUNBREUtQ09OVFJPTExFUi5SRUFESU5HLlJFQUQiLCJDUlBULUtNLU9SREVSUy5PUkRFUi1GQUNBREUtQ09OVFJPTExFUi5NT0RJRllJTkctRFJBRlQuV1JJVEUiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5MT0FOLlJFQUQiLCJDUlBULUtNLU9SREVSUy5PUkRFUi1GQUNBREUtQ09OVFJPTExFUi5SRUFESU5HLlJFQUQiLCJDUlBULUtNLU9SREVSUy5TVVotUkVHSVNUUlktRkFDQURFLUNPTlRST0xMRVIuREVMRVRJTkcuREVMRVRFIiwiQ1JQVC1LTS1PUkRFUlMuT1JERVItRkFDQURFLUNPTlRST0xMRVIuUkVBRElORy1CWS1TVVouUkVBRCIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLlJFTUFSS0lORy5SRUFEIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuQ1JPU1NCT1JERVIuUkVBRCIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLk9TVF9DT01QTEVURV9ERVNDUklQVElPTi5SRUFEIiwiRUxLLVJFR0lTVFJBVElPTi5DUkVBVEUiLCJDUlBULUxLLURPQy1BUEkuQVBQLVVTRVItQ09OVFJPTExFUi5XUklURSIsIkVMSy1SRUdJU1RSQVRJT04uUkVBRCIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLkFDQ0VQVEFOQ0UuQ1JFQVRFIiwiQ1JQVC1LTS1PUkRFUlMuTEFCRUwtVEVNUExBVEUtRkFDQURFLUNPTlRST0xMRVIuREVMRVRJTkcuREVMRVRFIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuSU5ESS1DT01NSVNTSU9OSU5HLkNSRUFURSIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLlNISVAtQ1JPU1NCT1JERVIuUkVBRCIsIkNSUFQtRkFDQURFLkRPQy1DT05UUk9MTEVSLk9TVF9ERVNDUklQVElPTi5SRUFEIiwiQ1JQVC1MSy1ET0MtQVBJLkJMT0NLSU5HLUNPTlRST0xMRVIuQ1JFQVRFIiwiQ1JQVC1GQUNBREUuRE9DLUNPTlRST0xMRVIuTFBfSU5UUk9EVUNFX09TVC5DUkVBVEUiLCJDUlBULUZBQ0FERS5ET0MtQ09OVFJPTExFUi5LTS1DQU5DRUwuQ1JFQVRFIl0sImNsaWVudF9pZCI6ImNycHQtc2VydmljZSIsImZ1bGxfbmFtZSI6ItCv0YDRi9Cz0LjQvdCwINCY0L3QtdGB0YHQsCDQktGP0YfQtdGB0LvQsNCy0L7QstC90LAiLCJzY29wZSI6WyJ0cnVzdGVkIl0sImlkIjo2MDAwMTUxMDcsImV4cCI6MTYwMzgyNjkyOSwib3JnYW5pc2F0aW9uX3N0YXR1cyI6IlJFR0lTVEVSRUQiLCJqdGkiOiJlNDc0ZGNhNS0zYTNlLTQ3NjEtOWJhMi00NGNkMDJjOGM5NzIifQ.n95TMK60WwY_XTJazC5gR4gBHy4nvNxLtrlL_3jvnU0"

DEBUG = True
# Декоратор для логов 
def log( f ):
    def new_func( *args, **kwargs ):
        if DEBUG:
            logging.info( "Вызов #%s#( #%s#, #%s# )"%( f.__name__, args, kwargs) )
        r = f( *args, **kwargs )
        if DEBUG:
            logging.info( "Возврат:#%s#"%( r ) )
        return( r )
    return new_func

class Ch_Znak_Api:
    ADDRESS = 'https://ismp.crpt.ru/api/v3/'
  
    def __init__( self, log, cfg ):
        self.log = log
        self.cfg = cfg
        self.log.info( "Конструктор Ch_Znak_Api" )
        self.command = {'get_question':self.get_question, 
                        'get_token':self.get_token, 
                        'certification':self.cert, 
                        'get_info':self.get_info, 
                        'get_gtins':self.get_gtins}

    def get_question( self, data ):
        self.log.info( "Запрос на строку для регистрации." )
        res = requests.get( self.ADDRESS + 'auth/cert/key' )
        if res.status_code == 200:
            r = res.json() 
            self.uuid = r['uuid']
            self.data = r['data']
            if 'filename' in data:
                with open( data['filename'], 'wt' ) as f:
                    f.write( r['data'] )
            result = {'Result':'OK', 'data':r}
        else:
            result = {'Result':'ERROR'}
        return result
    
    def cert( self, data ):
        self.log.info( "Подпись строки." )
        result = { 'Result':'ERROR' }
        if 'input' in data:
            if 'output' in data:
#                csptest -sfsign -sign -in F:\doc.txt -out F:\signed_doc.txt -my xxx@mail.ru -base64 -add
                os.system( '/opt/cprocsp/bin/amd64/csptest -sfsign -sign \
                   -in %s -out %s -my "96d6f5e1c15cfc3de2a1ad7952cc7640e995df2d"\
                   -base64 -add'%( data['input'], data['output'] ) ) 
                result = { 'Result':'OK', 'data':data }
        return result

    def get_token( self, data):
        self.log.info( "Получение токена." )
        result = {'Result':'ERROR'}
        if 'filename' in data:
            lines = open( data['filename'], 'rt' ).readlines()
            ecp = ''
            for i in lines:
               ecp = ecp + i.rstrip( ' \n' ) 
            
            hdr = { "Content-Type": "application/json; charset=UTF-8" }
            d = '{ "uuid":"%s","data":"%s" }'%(self.uuid, ecp)              
            logging.info( 'Headers:[%s]'%(hdr) )
            logging.info( 'Data:[%s]'%(d) )
            res = requests.post( self.ADDRESS + 'auth/cert/', headers = hdr, data = d ) 
            print( res )
            self.token = res.json()['token']
            result = {'Result':'OK', 'data':res.json()}
        return result
    
    def get_info(self, data):
        result = {'Result':'ERROR'}
        if 'cis' in data:
            res = requests.get( self.ADDRESS + 'facade/identifytools/info',
                                            headers = {'Authorization':'Bearer %s'%(self.token)}, 
                                            params = {'cis':'%s'%(data['cis']) }  )
            result = {'Result':'OK', 'data':res.json()}
        return result

    def get_gtins( self, data ):
        result = {'Result':'ERROR'}
        par = { 'pg':'shoes', 'limit':10000 }
        res = requests.get( self.ADDRESS + 'product/search',
                            headers = {'Authorization':'Bearer %s'%(self.token)}, 
                            params = par )
        result = {'Result':'OK', 'data':res.json()}
        return result


    def do(self, cmd, data):
        if cmd in self.command:
            result = self.command[cmd]( data ) 
            
        else:
            result = { 'Result':'ERROR', 'data':'Unknown command' }
        return result

if __name__ == "__main__":
    print( "Этот модуль является частью приложения." )
    print( "Для запуска приложения выполните main.py" )
    
#if __name__ == "__main__":
#    
#    logging.basicConfig( level = logging.INFO )
#    logging.info('Запуск')
#    api = Api()
#    print( api.do( 'get_question', {'filename':'out.txt' }) )
#    print( api.do( 'certification', { 'input':'out.txt', 'output':'ecp.txt' } ) )
#    print( api.do( 'get_token', {'filename':'ecp.txt'} ) )
##    print( api.do( 'get_info', {'cis':'010290000022918121eRakxUaN2rTdt'} ) )
#    res = ( api.do( 'get_gtins', {} ) )['data']['results']
#    print( '---------------------------' )
#    n = 0
#    for i in res:
#        
#        pos = i['name'].rfind( 'модель' )
#        s = i['name'][pos:len( i['name'] )]
#        mr = s.split( ',' )
#        s = i['gtin'] + '|' + mr[0][7:len( mr[0] )] + '|' + mr[1][8:len( mr[1] )]
#        print( s )
#        n = n + 1
#    print( 'Всего %s кодов.'%( n ) )
