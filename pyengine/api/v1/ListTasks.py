from pyengine.lib.error import *
from pyengine.lib.command import Command

class ListTasks(Command):

    # Request Parameter Info
    req_params = {
        'cluster_id': ('o', 'str'),
        'search': ('o', 'list'),
        'sort': ('o', 'dic'),
        'page': ('o', 'dic'),
        'res_params': ('o', 'list'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        search = self.makeSearch('cluster_id', 'status') 
        sort = self.params.get('sort', {'key': 'cluster_id'})
        page = self.params.get('page', {})
        res_params = self.params.get('res_params', [])

        mesos_mgr = self.locator.getManager('MesosManager')

        (task_infos, total_count) = mesos_mgr.listTasks(search, sort, page, res_params)

        response = {}
        #response['total_count'] = total_count
        response['data'] = task_infos

        return response
