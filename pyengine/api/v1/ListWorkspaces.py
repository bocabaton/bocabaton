from pyengine.lib.error import *
from pyengine.lib.command import Command

class ListWorkspaces(Command):

    # Request Parameter Info
    req_params = {
        'user_id': ('o', 'str'),
        'search': ('o', 'list'),
        'sort': ('o', 'dic'),
        'page': ('o', 'dic'),
        'res_params': ('o', 'list'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        search = self.makeSearch('user_id', 'status') 
        sort = self.params.get('sort', {'key': 'user_id'})
        page = self.params.get('page', {})
        res_params = self.params.get('res_params', [])

        ws_mgr = self.locator.getManager('WorkspaceManager')

        (ws_infos, total_count) = ws_mgr.listWorkspaces(search, sort, page, res_params)

        response = {}
        response['total_count'] = total_count
        response['data'] = []

        for ws_info in ws_infos:
            response['data'].append(ws_info.result(self.user_meta['timezone']))

        return response
