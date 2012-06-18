#!/usr/bin/env python

import sys,time
import signal
from signal import SIGTERM
from multiprocessing import Process
from salving_daemon import Daemon
from salving_proc import salving_proc
from salving_proc import proc


#main application		
class MyDaemon(Daemon):

	def run(self):
		signal.signal(signal.SIGCHLD, signal.SIG_IGN)
		id_list = []
		while True:
			sproc = salving_proc(self.logger)
			proclist = sproc.get_proc_list()
			#if this task not exists in id_list, init the process
			for data in proclist:
				if(data['id'] not in id_list):
					id = data['id']
					child_proc = proc()
					p = Process(target = child_proc.run, args=(id,))
					p.start()
					id_list.append(id)
					
			#clean id list
			for id in id_list:
				flag = False
				for data in proclist:
					if(data['id'] == id):
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
