#!/usr/bin/python3
# -*- codingtype=utf-8-*-

import config
import log

CONFIG_FILE_NAME = "znak.ini"

if __name__ == "__main__":
    cfg = config.Configuration( CONFIG_FILE_NAME )
    log = log.Log( cfg )
    log.info( "Hello" )
