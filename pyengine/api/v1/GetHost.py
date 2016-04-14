from pyengine.lib.error import *
from pyengine.lib.command import Command

class GetHost(Command):

    # Request Parameter Info 
    req_params = {
        'host_id': ('o', 'str'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        infra_mgr = self.locator.getManager('InfraManager')

        host_info = infra_mgr.getHost(self.params['host_id'])

        return host_info
