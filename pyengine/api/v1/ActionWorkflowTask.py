import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class ActionWorkflowTask(Command):

    # Request Parameter Info
    req_params = {
        'get': ('o', 'dic'),
        'add': ('o', 'dic')
    }

    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        wf_mgr = self.locator.getManager('WorkspaceManager')

        if self.params.has_key("add"):
            task = wf_mgr.addWorkflowTask(self.params)
        elif self.params.has_key("get"):
            task = wf_mgr.getWorkflowTask(self.params)

        return task.result(self.user_meta['timezone'])

