import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class CreateCluster(Command):

    # Request Parameter Info 
    req_params = {
        'name': ('r', 'str'),
        'zone_id': ('r', 'str'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        infra_mgr = self.locator.getManager('InfraManager')

        cluster_info = infra_mgr.createCluster(self.params)

        return cluster_info.result(self.user_meta['timezone'])
