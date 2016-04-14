import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class CreateWorkspace(Command):

    # Request Parameter Info 
    req_params = {
        'user_id'   : ('r', 'str'),
        'name'      : ('r', 'str'),
        'owner'     : ('o', 'list')
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        ws_mgr = self.locator.getManager('WorkspaceManager')

        ws_info = ws_mgr.createWorkspace(self.params)
        
        return ws_info.result(self.user_meta['timezone'])
