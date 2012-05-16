#!/usr/bin/env python

import sys, time
from multiprocessing import Process
from salving_daemon import Daemon

class MyDaemon(Daemon):
	
	def po(self):
		while True:
			self.logger.info("child process is running....")	
			time.sleep(3600)

	def run(self):
		while True:
			if(len(self.processes_list)<3):
				p = Process(target=self.po)
				p.start()
				#p.join()
				self.processes_list.append(p.pid)
				self.logger.info("process name is %s", p.name)
				self.logger.info("process id is %s", str(p.pid))
			time.sleep(1)

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
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
