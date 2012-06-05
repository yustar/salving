#!/usr/bin/env python
#-*- coding: utf8 -*-

import os.path
import MySQLdb
import MySQLdb.cursors
import ConfigParser
import salving_logger

class database:

	_dbhost = ""
	_dbuser = ""
	_dbpassword = ""
	_dbname = ""
	_dbport = ""
	_dbcharset = ""

	_conn = ""
	_cursor = ""

	def __init__(self, dbtype, logger):
		config = ConfigParser.ConfigParser()
		config.read(os.path.split(os.path.realpath(__file__))[0]+"/salving.conf")
		if(dbtype == None):
			db = "basic_database"
		else:
			db = dbtype
		self._dbhost = config.get(db, 'dbhost')
		self._dbname = config.get(db, 'dbname')
		self._dbuser = config.get(db, 'dbuser')
		self._dbpassword = config.get(db, 'dbpassword')
		self._dbcharset = config.get(db, 'dbcharset')
		self._dbport = int(config.get(db, "dbport"))
		self._conn = self.connectMySQL()
		self.logger = logger


	#mysql connect
	def connectMySQL(self):
		conn = False
		try:
			conn = MySQLdb.connect(host=self._dbhost,
					user=self._dbuser,
					passwd=self._dbpassword,
					db=self._dbname,
					port=self._dbport,
					cursorclass=MySQLdb.cursors.DictCursor,
					charset=self._dbcharset,
					)
		except Exception,data:
			self.logger.error("connect database failed, %s" % data)
			conn = False
		return conn


	#get the query result set
	def fetch_all(self, sql):
		res = ''
		if(self._conn!=False):
			try:
				self._cursor = self._conn.cursor()
				self._cursor.execute(sql)
				res = self._cursor.fetchall()
			except Exception, data:
				res = False
				self.logger.warn("query database exception, %s" % data)
		return res


	def update(self, sql):
		flag = False
		if(self._conn!=False):
			try:
				self._cursor = self._conn.cursor()
				self._cursor.execute(sql)
				self._conn.commit()
				flag = True
			except Exception, data:
				flag = False
				self.logger.warn("update database exception, %s" % data)

		return flag

	#close database connection
	def close(self):
		if(self._conn!=False):
			try:
				if(type(self._cursor)=='object'):
					self._cursor.close()
				if(type(self._conn)=='object'):
					self._conn.close()
			except Exception, data:
				self.logger.warn("close database exception, %s,%s,%s" % (data, type(self._cursor), type(self._conn)))

#get database class	
def db(dbname, logger):
	db = database(dbname, logger)
	return db
