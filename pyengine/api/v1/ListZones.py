from pyengine.lib.error import *
from pyengine.lib.command import Command

class ListZones(Command):

    # Request Parameter Info
    req_params = {
        'name': ('o', 'str'),
        'region_uuid': ('o', 'str'),
        'status': ('o', 'str'),
        'search': ('o', 'list'),
        'sort': ('o', 'dic'),
        'page': ('o', 'dic'),
        'res_params': ('o', 'list'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        search = self.makeSearch('name', 'status') 
        sort = self.params.get('sort', {'key': 'name'})
        page = self.params.get('page', {})
        res_params = self.params.get('res_params', [])

        infra_mgr = self.locator.getManager('InfraManager')

        (zone_infos, total_count) = infra_mgr.listZones(search, sort, page, res_params)

        response = {}
        response['total_count'] = total_count
        response['results'] = []

        for zone_info in zone_infos:
            response['results'].append(zone_info.result(self.user_meta['timezone']))

        return response
