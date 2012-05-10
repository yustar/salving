#!/usr/bin/python
# -*- coding: utf-8 -*-
#python log module
import logging.config
from logging.handlers import RotatingFileHandler
import ConfigParser
import os.path


#logging.basicConfig(
#		level = logging.INFO,
#		)

#log setting
def logger():
	config = ConfigParser.ConfigParser()
	config.read(os.path.split(os.path.realpath(__file__))[0]+"/analysis.conf")
	format       = config.get("log", "format").replace('@', '%')
	name         = config.get("log", "name")
	backupcount  = int(config.get("log", "backupcount"))
	maxbytes     = int(config.get("log", "maxbytes"))

	logger = logging.getLogger()
	Rthandler = RotatingFileHandler(os.path.split(os.path.realpath(__file__))[0]+'/'+name, 
			maxBytes=maxbytes,
			backupCount=backupcount)
	Rthandler.setLevel(logging.INFO)
	formatter = logging.Formatter(format)
	Rthandler.setFormatter(formatter)
	logger.addHandler(Rthandler)
	return logger

if __name__ == "__main__":
	print "This program is being run by itself"

version = "1.0.1"
