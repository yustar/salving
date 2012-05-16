#!/usr/bin/python
# -*- coding: utf-8 -*-
#python log module
"""
logging model 
level logging's level notset(0) debug(10) info(20) warning(30)
error(40) critical(50)
"""
import logging
from logging.handlers import RotatingFileHandler
import ConfigParser
import os.path

#log setting
def logger():
	config = ConfigParser.ConfigParser()
	config.read(os.path.split(os.path.realpath(__file__))[0]+"/salving.conf")
	format       = config.get("log", "format").replace('@', '%')
	name         = config.get("log", "name")
	backupcount  = int(config.get("log", "backupcount"))
	maxbytes     = int(config.get("log", "maxbytes"))
	level        = int(config.get("log", "level"))

	logger = logging.getLogger()
	logger.setLevel(level)
	Rthandler = RotatingFileHandler(os.path.split(os.path.realpath(__file__))[0]+'/'+name,
			maxBytes=maxbytes,
			backupCount=backupcount)
	formatter = logging.Formatter(format)
	Rthandler.setFormatter(formatter)
	logger.addHandler(Rthandler)
	return logger

if __name__ == "__main__":
	#test this logging model
	log = logger()
	log.debug("test logging model")

version = "1.0.1"
