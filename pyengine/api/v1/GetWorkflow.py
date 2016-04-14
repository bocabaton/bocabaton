import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class GetWorkflow(Command):

    # Request Parameter Info 
    req_params = {
        'name': ('r', 'str')
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        #workflow_mgr = self.locator.getManager('WorkflowManager')

        #workflow_info = workflow_mgr.getWorkflow(self.params)
        workflow_info="""
<xml>
test
</xml>
"""
        return workflow_info
