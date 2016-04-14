import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class DeployWorkflow(Command):

    # Request Parameter Info 
    req_params = {
        'user_id'   : ('r', 'str'),
        'workspace_id'   : ('r', 'str'),
        'workflow_id'      : ('r', 'str'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        ws_mgr = self.locator.getManager('WorkspaceManager')

        wf_info = ws_mgr.deployWorkflow(self.params)
        
        return wf_info.result(self.user_meta['timezone'])
