#!/usr/bin/python
# -*- coding: utf-8 -*-
# Task class 

import os.path
import pycurl
import analysis_db
import analysis_xml
import datetime
from   datetime import timedelta, date
import socket
import struct
import signal
import sys

#Task Base Class
class Task:
	def run_task(self):
		"""virtual method, in the subclass"""

	def notify(self):
		"""Server-side message notification"""


#Task Sub Class 
class MyTask(Task):
	def __init__(self):
		"""init args of the sub class"""
		
	def run_task(self):
		logging.info("run task in sub-process ")
		

def create_task():
	my_task = None
	my_task = MyTask()
	return my_task
