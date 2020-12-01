#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import requests
import os
# import json

token = ""

DEBUG = True


# Декоратор для логов
def log(f):
    def new_func(*args, **kwargs):
        if DEBUG:
            logging.info("Вызов #%s#( #%s#, #%s# )" % (f.__name__, args, kwargs))
        r = f(*args, **kwargs)
        if DEBUG:
            logging.info("Возврат:#%s#" % (r))
        return(r)
    return new_func


class Ch_Znak_Api:
    ADDRESS = 'https://ismp.crpt.ru/api/v3/'
  
    def __init__(self, log, cfg):
        self.log = log
        self.cfg = cfg
        self.log.info("Конструктор Ch_Znak_Api")
        self.command = {'get_question': self.get_question,
                        'get_token': self.get_token,
                        'certification': self.cert,
                        'get_info': self.get_info,
                        'get_gtins': self.get_gtins}

    def get_question(self, data):
        self.log.info("Запрос на строку для регистрации.")
        res = requests.get(self.ADDRESS + 'auth/cert/key')
        if res.status_code == 200:
            r = res.json() 
            self.uuid = r['uuid']
            self.data = r['data']
            if 'filename' in data:
                with open(data['filename'], 'wt') as f:
                    f.write(r['data'])
            result = {'Result': 'OK', 'data': r}
        else:
            result = {'Result': 'ERROR'}
        return result
    
    def cert(self, data):
        self.log.info("Подпись строки.")
        result = {'Result': 'ERROR'}
        if 'input' in data:
            if 'output' in data:
                os.system('/opt/cprocsp/bin/amd64/csptest -sfsign -sign \
                   -in %s -out %s -my "96d6f5e1c15cfc3de2a1ad7952cc7640e995df2d"\
                   -base64 -add' % (data['input'], data['output']))
                result = {'Result': 'OK', 'data': data}
        return result

    def get_token(self, data):
        self.log.info("Получение токена.")
        result = {'Result': 'ERROR'}
        if 'filename' in data:
            lines = open(data['filename'], 'rt').readlines()
            ecp = ''
            for i in lines:
                ecp = ecp + i.rstrip(' \n')
            
            hdr = {"Content-Type": "application/json; charset=UTF-8"}
            d = '{ "uuid":"%s","data":"%s" }' % (self.uuid, ecp)
            logging.info('Headers:[%s]' % (hdr))
            logging.info('Data:[%s]' % (d))
            res = requests.post(self.ADDRESS + 'auth/cert/', headers=hdr, data=d)
            print(res)
            self.token = res.json()['token']
            result = {'Result': 'OK', 'data': res.json()}
        return result
    
    def get_info(self, data):
        result = {'Result': 'ERROR'}
        if 'cis' in data:
            res = requests.get(self.ADDRESS + 'facade/identifytools/info',
                               headers={'Authorization': 'Bearer %s' % (self.token)},
                               params={'cis': '%s' % (data['cis'])})
            result = {'Result': 'OK', 'data': res.json()}
        return result

    def get_gtins(self, data):
        result = {'Result': 'ERROR'}
        par = {'pg': 'shoes', 'limit': 10000}
        res = requests.get(self.ADDRESS + 'product/search',
                           headers={'Authorization': 'Bearer %s' % (self.token)},
                           params=par)
        result = {'Result': 'OK', 'data': res.json()}
        return result

    def do(self, cmd, data):
        if cmd in self.command:
            result = self.command[cmd](data)
        else:
            result = {'Result': 'ERROR', 'data': 'Unknown command'}
        return result


if __name__ == "__main__":
    print("Этот модуль является частью приложения.")
    print("Для запуска приложения выполните main.py")
    
# if __name__ == "__main__":
#    
#    logging.basicConfig( level = logging.INFO )
#    logging.info('Запуск')
#    api = Api()
#    print( api.do( 'get_question', {'filename':'out.txt' }) )
#    print( api.do( 'certification', { 'input':'out.txt', 'output':'ecp.txt' } ) )
#    print( api.do( 'get_token', {'filename':'ecp.txt'} ) )
#    print( api.do( 'get_info', {'cis':'010290000022918121eRakxUaN2rTdt'} ) )
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
