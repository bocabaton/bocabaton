import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class CreateWorkflow(Command):

    # Request Parameter Info 
    req_params = {
        'workspace_id'   : ('r', 'str'),
        'name'      : ('r', 'str'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        ws_mgr = self.locator.getManager('WorkspaceManager')

        wf_info = ws_mgr.createWorkflow(self.params)
        
        return wf_info.result(self.user_meta['timezone'])
