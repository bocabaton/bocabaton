from pyengine.info import Info
from pyengine.lib.error import *

class UserInfo(Info):

    def __init__(self, vo, options):
        super(self.__class__, self).__init__(vo, options)
        self.fetchByID()

    def __repr__(self):
        return '<UserInfo: %s>' %self.vo.user_id 

    def fetchByID(self):
        """
        Fetch needed data from vo
        """
        if self.checkResponseParams():
            try:
                for p in self.options['res_params']:
                    self.output[p] = self.vo.__dict__[p]

            except:
                raise ERROR_INVALID_PARAMETER(key='res_params', value=p)

        else:
            self.output['user_id'] = self.vo.user_id
            self.output['name'] = self.vo.name
            self.output['state'] = self.vo.state
            self.output['email'] = self.vo.email
            self.output['language'] = self.vo.language
            self.output['timezone'] = self.vo.timezone
            self.output['created'] = self.vo.created
