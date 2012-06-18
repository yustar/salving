#!/usr/bin/env python
import salving_logger, time
import salving_db

#proc manage
class salving_proc:
    
    def __init__(self, logger):
        self.logger = logger
        
    #Get Configure info
    def getConf(self):
		'''
		get proc configuration
		'''	
		self.logger.info('get proc configuration...')
    
    def get_proc_list(self):
        #main proc
		res = [{"id":1}, {"id":2}]
		return res

#children process init funcion  
class proc(salving_proc):
    
    def __init__(self):
        '''
        '''

        
    def run(self, id):
        self.logger = salving_logger.logger("salving_%d.log" % id)
        while(True):
            self.logger.info(id)
            time.sleep(30)
        return None
