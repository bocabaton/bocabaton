import datetime

from django.contrib.auth.hashers import make_password
from pyengine.lib import utils
from pyengine.lib import config
from pyengine.lib.error import *
from pyengine.manager import Manager 

from pyengine.lib.restclient import RestClient

class MesosManager(Manager):

    GLOBAL_CONF = config.getGlobalConfig()

    def getActivatedSlaves(self):
        # TODO: needs to find actual master using zookeeper
        client = RestClient('127.0.0.1', port=5050)
        (code, result) = client.request('GET',url='/state.json')
        self.logger.debug("MESOS(%s):%s" % (type(result), result) )
        if code == 200:
            self.logger.debug("MESOS:%s" % result)
            output = {}
            output['activated_slaves'] = int(result['activated_slaves'])
            output['slaves'] = result['slaves']
            return output

        else:
            raise ERROR_NOT_FOUND(key='mesos', value='/state.json')            

    def getMesosInfo(self):
        # TODO: needs to find actual master using zookeeper
        # Loop every mesos master
        # TODO: get masters
        masters = ["10.240.0.3", "104.197.10.135"]
        (c0, m0, d0) = (0.0,0,0)
        (c1, m1, d1) = (0.0,0,0)
        output = {'num_of_frameworks':0, 'activated_slaves':0, 'num_of_tasks':0}

        for master in masters:
            self.logger.debug("#### loop %s" % master)
            client = RestClient(master, port=5050)
            (code, result) = client.request('GET',url='/state.json', content_type='json')
            self.logger.debug("MESOS(%s):%s" % (type(result), result) )
            if code == 200:
                self.logger.debug("MESOS:%s" % result)
                output['num_of_frameworks'] = output['num_of_frameworks'] + len(result['frameworks'])
                output['activated_slaves'] = output['activated_slaves'] + int(result['activated_slaves'])
                tasks = result['frameworks'][0]['tasks']
                output['num_of_tasks'] = output['num_of_tasks'] + len(tasks)
                # calculate Sum of CPU, Memory, Disk
                slaves = result['slaves']
                for slave in slaves:
                    if slave['active'] == True:
                        c1 = c1 + slave['resources']['cpus']
                        m1 = m1 + slave['resources']['mem']
                        d1 = d1 + slave['resources']['disk']
                        c0 = c0 + slave['used_resources']['cpus']
                        m0 = m0 + slave['used_resources']['mem']
                        d0 = d0 + slave['used_resources']['disk']
            else:
                self.logger.debug("### This IP is not mesos master:%s" % master)            


        output['compute'] = {'resources':{'cpus':c1, 'mem':m1/1000, 'disk':d1/1000},
                            'used_resources':{'cpu':c0, 'mem':m0/1000, 'disk':d0/1000}}
        return output

        
    def listTasks(self, search, sort, page, rest_params):
        # TODO: needs to find actual master using zookeeper
        masters = ["10.240.0.3", "104.197.10.135"]
        output = []
        for master in masters:
            client = RestClient(master, port=5050)
            (code, result) = client.request('GET',url='/state.json', content_type='json')
            self.logger.debug("MESOS(%s):%s" % (type(result), result) )
            slave_dic = {}
            if code == 200:
                self.logger.debug("MESOS:%s" % result)
                #r_dic = json.loads(result)
                tasks = result['frameworks'][0]['tasks']
                slaves = result['slaves']
                for slave in slaves:
                    slave_dic[slave['id']] = slave['hostname']
                self.logger.info(str(slave_dic))
                self.logger.info(str(tasks))
                for task in tasks:
                    task_dic = {}
                    task_dic['id'] = task['id']
                    task_dic['name'] = task['name']
                    task_dic['compute'] = slave_dic[task['slave_id']]
                    #task_dic['ip'] = '1.2.3.4'
                    task_dic['ip'] = task['statuses'][0]['container_status']['network_infos'][0]['ip_address']
                    task_dic['status'] = task['state']
                    task_dic['created'] = datetime.datetime.fromtimestamp(task['statuses'][0]['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    output.append(task_dic) 
        return (output, len(output)) 


