from pyengine.lib.error import *
from pyengine.lib.command import Command

class ListNodes(Command):
    # Request Parameter Info 
    req_params = {
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)


    def execute(self):
        mesos_mgr = self.locator.getManager('MesosManager')
        mesos_info = mesos_mgr.getActivatedSlaves()
        return mesos_info
