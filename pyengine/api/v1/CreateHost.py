import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class CreateHost(Command):

    # Request Parameter Info 
    req_params = {
        'name': ('r', 'str'),
        'domain': ('o', 'str'),
        'ipv4': ('r', 'str'),
        'user_id': ('r', 'str'),
        'password': ('r', 'str'),
        'id_rsa': ('o', 'str'),
        'id_dsa': ('o', 'str'),
        'cluster_id': ('r', 'str')
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        infra_mgr = self.locator.getManager('InfraManager')

        host_info = infra_mgr.createHost(self.params)

        return host_info
