from pyengine.lib.error import *
from pyengine.lib.command import Command

class GetZone(Command):

    # Request Parameter Info 
    req_params = {
        'zone_id': ('o', 'str'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        infra_mgr = self.locator.getManager('InfraManager')

        zone_info = infra_mgr.getZone(self.params)

        return zone_info.result(self.user_meta['timezone'])
