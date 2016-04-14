from django.contrib.auth.hashers import make_password
from pyengine.lib import utils
from pyengine.lib import config
from pyengine.lib.error import *
from pyengine.manager import Manager 

from pyengine.lib.restclient import RestClient

class SingularityManager(Manager):

    GLOBAL_CONF = config.getGlobalConfig()

    # param:
    # r_dic : dictionary for singularity request
    # sample :
    # {
    #    "id": "dragon fly",
    #    "owners": [
    #        "choonho.son@gamil.com"
    #    ],
    #    "daemon": True,
    #    "rackSensitive": False,
    #    "loadBalanced": False
    # }
    def createRequest(self, r_dic, endpoint='127.0.0.1'):
        # TODO:
        client = RestClient(endpoint,port=7099)
        s_url='/singularity/api/requests'
        (code,result) = client.request('POST', url=s_url, params=r_dic, content_type="json")
        self.logger.debug("Singularity(%s): %s" % (code,result))
        if code == 200:
            self.logger.debug("Singularity(request): %s" % result)
            return result
        else:
            raise ERROR_NOT_FOUND(key="singularity", value=r_dic)
 
        # Connect to singularity

        # Call request API

        # return result


    def deployTask(self, r_dic, endpoint='127.0.0.1'):
        # TODO:
        client = RestClient(endpoint, port=7099)
        s_url='/singularity/api/deploys'
        (code, result) = client.request('POST', url=s_url, params=r_dic, content_type="json")
        self.logger.debug("Singularity(%s): %s" % (code, result))
        if code == 200:
            return result
        else:
            raise ERROR_NOT_FOUND(key="singularity", value=r_dic)

    def checkPending(self):
        client = RestClient('127.0.0.1', port=7099)
        s_url = '/singularity/api/deploys/pending'
        (code, result) = client.request('GET', url=s_url, content_type="json")
        if code == 200:
            return result
        else:
            raise ERROR_NOT_FOUND(key="singularity", value=s_url)
