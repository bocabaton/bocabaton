import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class BpmnTask(Command):

    # Request Parameter Info
    req_params = {
        'get': ('o', 'dic'),
        'add': ('o', 'dic'),
        'deploy': ('o', 'dic')
    }

    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        wf_mgr = self.locator.getManager('WorkspaceManager')

        if self.params.has_key("add"):
            pass
        elif self.params.has_key("get"):
            pass
        elif self.params.has_key("deploy"):
            task = wf_mgr.deployBpmnTask(self.params) 

        return task

