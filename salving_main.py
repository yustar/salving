#!/usr/bin/env python

import sys, time, commands,re,datetime
import signal
import salving_db
from signal import SIGTERM
from multiprocessing import Process
from salving_daemon import Daemon
import ConfigParser
import os.path
from os.path import exists
from datetime import timedelta, date
import salving_logger

class Task:
		
	def get_tasklist(self, type, logger):
		#defined task list
		res = [{"id":1}, {"id":2}]
		return res

		
class MyDaemon(Daemon):
	
	#count today data		
	def run_task(self, data):
		INIT_TIME = None
		sublogger = salving_logger.logger("salving_%s.log" % data['id'])
		#check this subprocess status
		while True:
			sublogger.info("child process is running")
			now_time = (date.today()-timedelta(days=1)).strftime("%Y-%m-%d")
			hour = int(time.strftime('%H', time.localtime(time.time())))
			sublogger.info(type(hour))
			#task begin from every data 8:00
			if hour>8:
				#task every day only run one time
				if(now_time != INIT_TIME):
					INIT_TIME = now_time
					
			time.sleep(30)

	def run(self):
		signal.signal(signal.SIGCHLD, signal.SIG_IGN)
		id_list = []
		while True:
			task = Task()
			tasklist = task.get_tasklist(self.logger)
			#if this task not exists in id_list, init the process
			for data in tasklist:
				if(data['id'] not in id_list):
					p = Process(target = self.run_task, args=(data,))
					p.start()
					id_list.append(data['id'])
			#clean id list
			for id in id_list:
				flag = False
				for task in tasklist:
					if(task['id'] == id):
						flag = True
				if(flag == False):
					id_list.remove(id)		
			time.sleep(30)

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/salving.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
