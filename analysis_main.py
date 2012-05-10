#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author yustarwang
date   2012-05-10
"""

import sys, os, time, atexit
from signal import SIGTERM
import ConfigParser
import os
import analysis_logger
import analysis_db
import analysis_task
import analysis_xml
from datetime import timedelta, date
import signal

class Daemon:
	"""
	A generic daemon class.

	Usage: subclass the Daemon class and override the _run() method
	"""
	def __init__(self, process_id, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.process_id = process_id
		self.pidfile="analysis_" + self.process_id + ".pid"
	def _daemonize(self):

		#logging.info("fork #1 begin")
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
			logging.info("fork #1 failed: (%s)", e.strerror)
			sys.exit(1)

		logging.info("fork #1 over")
		#leave the terminal
		os.setsid()
		#change dir
		os.chdir(os.getcwd())
		#modify the current directory creation permissions
		os.umask(0)

		logging.info("fork #2 begin")
		#prohibit the process to re-open the control terminal
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
			logging.info("fork #2 failed: (%s)", e.strerror)
			sys.exit(1)
		logging.info("fork #2 over")
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)

		logging.info('fork subprocess')
		#redirect standard input / output / error
		try:
			os.dup2(si.fileno(), sys.stdin.fileno())
			os.dup2(so.fileno(), sys.stdout.fileno())
			os.dup2(se.fileno(), sys.stderr.fileno())
		except OSError, e:
			sys.stderr.write("os error")

		#a function of the exit of the registration process, delete the pid file
		atexit.register(self.delpid)
		pid = str(os.getpid())
		logging.info("pidfile:%s,pid:%s",self.pidfile,pid)
		file(self.pidfile,'w+').write("%s\n" % pid)

	def delpid(self):
		logging.info("remove pidfile:%s",self.pidfile)
		try:
			os.remove(self.pidfile)
		except OSError, e:
			sys.stderr.write("No such file or directory")

	def start(self):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already runs
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError, e:
			pid = None

		if pid:
			message = "pidfile %s already exist. Daemon already running?\n"
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)
		pid = str(os.getpid())
		# Start the daemon
		logging.info("start to call _daemonize")
		self._daemonize()
		logging.info("start to call _run")
		self._run()
		logging.info("call _run over")
		
	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			print os.getcwd()
			message = "pidfile %s does not exist. Daemon not running?\n"
			sys.stderr.write(message % self.pidfile)
			return # not an error in a restart
		# Try killing the daemon process
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			print str(err)
			sys.exit(1)

	def _run(self):
		"""
		You should override this method when you subclass Daemon. It will be called after the process has been
		daemonized by start() or restart().
		"""

#init sub-process
class MyDaemon(Daemon):
	def __init__(self, process_id):
		Daemon.__init__(self, process_id)

	def _run(self):
		task=analysis_task.create_task()
		if task == None:
			sys.exit(1)
		while True:
			task.run_task()
			# 5 minutes count data
			time.sleep(6)
			
#Task Manager init subprocess
class TaskManager():
	def __init__(self):
		self.pidfile="analysis.pid"
	def delpid(self):
		logging.info("remove pidfile:%s",self.pidfile)
		os.remove(self.pidfile)
	def start(self):
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError, e:
			pid = None

		if pid:
			try:
				while 1:
					os.kill(pid, SIGTERM)
					time.sleep(0.1)
			except OSError, err:
				print str(err)
				#os.remove(self.pidfile)

		#atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile,'w+').write("%s\n" % pid)
		signal.signal(signal.SIGCHLD,signal.SIG_IGN)
		while True:
			process_list = ["1","2","3"] 
			for process_id in process_list:
				pid = os.fork()
				if(0 == pid):
					daemon = MyDaemon(process_id)
					if daemon:
						daemon.start()
					else:
						logging.info("create process to handle id:%d fail",process_id)
			time.sleep(30)
	def stop(self):
		process_list = ["1","2","3"]
		"""
		Stop all daemon process
		"""
		# Get the pid from the pidfile
		for process_id in process_list:
			logging.info("stop process:%s\n" %process_id)
			pidfile="analysis_" + process_id + ".pid"
			try:
				pf = file(pidfile,'r')
				pid = int(pf.read().strip())
				pf.close()
			except IOError,err:
				print str(err)
				continue
			try:
				while 1:
					os.kill(pid, SIGTERM)
					time.sleep(0.1)
			except OSError, err:
				#print str(err)
				os.remove(pidfile)
		logging.info("stop all child proc succ!")
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError, e:
			pid = None

		if pid:
			try:
				while 1:
					os.kill(pid, SIGTERM)
					time.sleep(0.1)
			except OSError, err:
				#print str(err)
				os.remove(self.pidfile)
				logging.info("stop the main proc succ!")

	def restart(self):
		"""
		Restart all the  daemon
		"""
		self.stop()
		time.sleep(1)
		self.start()
		
if __name__ == "__main__":
	task_mgr = TaskManager()
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			task_mgr.start()
		elif 'stop' == sys.argv[1]:
			task_mgr.stop()
			sys.exit(0)
		elif 'restart' == sys.argv[1]:
			task_mgr.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
