from django.contrib.auth.hashers import make_password
from pyengine.lib import utils
from pyengine.lib import config
from pyengine.lib.error import *
from pyengine.manager import Manager 

import paramiko
import pytz
import StringIO
from datetime import datetime

class InfraManager(Manager):

    GLOBAL_CONF = config.getGlobalConfig()

    ########################################
    # CreateXXX
    ########################################
    def createRegion(self, params):
        region_dao = self.locator.getDAO('region') 

        if region_dao.isExist(name=params['name']):
            raise ERROR_EXIST_RESOURCE(key='name', value=params['name'])

        dic = {}
        dic['name'] = params['name']

        region = region_dao.insert(dic)

        return self.locator.getInfo('RegionInfo', region)

    def createZone(self, params):
        # exist region
        region_dao = self.locator.getDAO('region')
        if region_dao.isExist(uuid=params['region_id']) == False:
            raise ERROR_EXIST_RESOURCE(key='region', value=params['region_id'])
        
        zone_dao = self.locator.getDAO('zone') 
        if zone_dao.isExist(name=params['name']):
            raise ERROR_EXIST_RESOURCE(key='name', value=params['name'])

        dic = {}
        dic['name'] = params['name']
        dic['region_uuid'] = params['region_id']
        zone = zone_dao.insert(dic)

        return self.locator.getInfo('ZoneInfo', zone)

    def createCluster(self, params):
        # exist zone
        zone_dao = self.locator.getDAO('zone')
        if zone_dao.isExist(uuid=params['zone_id']) == False:
            raise ERROR_EXIST_RESOURCE(key='zone', value=params['zone_id'])
        
        cluster_dao = self.locator.getDAO('cluster') 
        if cluster_dao.isExist(name=params['name']):
            raise ERROR_EXIST_RESOURCE(key='name', value=params['name'])

        dic = {}
        dic['name'] = params['name']
        dic['zone_uuid'] = params['zone_id']
        cluster = cluster_dao.insert(dic)

        return self.locator.getInfo('ClusterInfo', cluster)

    def createHost(self, params):
        # exist cluster
        cluster_dao = self.locator.getDAO('cluster')
        if cluster_dao.isExist(uuid=params['cluster_id']) == False:
            raise ERROR_EXIST_RESOURCE(key='cluster', value=params['cluster_id'])
        
        host_dao = self.locator.getDAO('host') 
        if host_dao.isExist(name=params['name']):
            raise ERROR_EXIST_RESOURCE(key='name', value=params['name'])

        dic = {}
        dic['name'] = params['name']
        dic['ipv4'] = params['ipv4']
        dic['user_id'] = params['user_id']
        if params.has_key('password'):
            dic['password'] = params['password']
        if params.has_key('id_rsa'):
            dic['id_rsa'] = params['id_rsa']
        if params.has_key('id_dsa'):
            dic['id_dsa'] = params['id_dsa']
        if params.has_key('domain'):
            dic['domain'] = params['domain']

        dic['cluster_uuid'] = params['cluster_id']
        host = host_dao.insert(dic)

        return self.getHost(host.uuid)

    ################################################
    # ListXXX
    ################################################
    def listRegions(self, search, sort, page, res_params):
        region_dao = self.locator.getDAO('region')

        output = []
        (regions, total_count) = region_dao.select(search=search, sort=sort, page=page)

        for region in regions:
            region_info = self.locator.getInfo('RegionInfo', region, res_params=res_params)
            output.append(region_info)

        return (output, total_count)

    def listZones(self, search, sort, page, res_params):
        zone_dao = self.locator.getDAO('zone')
        region_dao = self.locator.getDAO('region')

        output = []
        (zones, total_count) = zone_dao.select(search=search, sort=sort, page=page)

        for zone in zones:
            zone_info = self.locator.getInfo('ZoneInfo', zone, res_params=res_params)
            output.append(zone_info)

        return (output, total_count)

    def listClusters(self, search, sort, page, res_params):
        cluster_dao = self.locator.getDAO('cluster')

        output = []
        (clusters, total_count) = cluster_dao.select(search=search, sort=sort, page=page)

        for cluster in clusters:
            cluster_info = self.locator.getInfo('ClusterInfo', cluster, res_params=res_params)
            output.append(cluster_info)

        return (output, total_count)

    def listHosts(self, search, sort, page, res_params):
        host_dao = self.locator.getDAO('host')

        output = []
        (hosts, total_count) = host_dao.select(search=search, sort=sort, page=page)

        for host in hosts:
            host_dic = self.getHost(host.uuid)
            output.append(host_dic)

        return (output, total_count)


    ####################################################
    # getXXX
    ####################################################
    def getRegion(self, params):
        region_dao = self.locator.getDAO('region')

        if params.has_key('region_id'):
            regions = region_dao.getVOfromKey(uuid=params['region_id'])
            if regions.count() == 0:
                raise ERROR_NOT_FOUND(key='region_id', value=params['region_id'])

        else:
            raise ERROR_REQUIRED_PARAM(key='region_id')

        return self.locator.getInfo('RegionInfo', regions[0])

    def getZone(self, params):
        zone_dao = self.locator.getDAO('zone')

        if params.has_key('zone_id'):
            zones = zone_dao.getVOfromKey(uuid=params['zone_id'])
            if zones.count() == 0:
                raise ERROR_NOT_FOUND(key='zone_id', value=params['zone_id'])

        else:
            raise ERROR_REQUIRED_PARAM(key='zone_id')

        return self.locator.getInfo('ZoneInfo', zones[0])

    def getCluster(self, params):
        cluster_dao = self.locator.getDAO('cluster')

        if params.has_key('cluster_id'):
            clusters = cluster_dao.getVOfromKey(uuid=params['cluster_id'])
            if clusters.count() == 0:
                raise ERROR_NOT_FOUND(key='cluster_id', value=params['cluster_id'])

        else:
            raise ERROR_REQUIRED_PARAM(key='cluster_id')

        return self.locator.getInfo('ClusterInfo', clusters[0])

    ##############################################
    # Get Host
    # param: host_id
    # return: dictionary
    ##############################################
    def getHost(self, host_id):
        host_dao    = self.locator.getDAO('host')
        cluster_dao = self.locator.getDAO('cluster')
        zone_dao    = self.locator.getDAO('zone')
        region_dao  = self.locator.getDAO('region')

        hosts = host_dao.getVOfromKey(uuid=host_id)
        if hosts.count() == 0:
            raise ERROR_NOT_FOUND(key='host_id', value=params['host_id'])
        host = {}
        # Temp (Choonho Son)
        host['name'] = hosts[0].name
        host['host_id'] = str(hosts[0].uuid)
        if hosts[0].domain:
            host['domain'] = hosts[0].domain
        host['ipv4'] = hosts[0].ipv4
        host['created'] = hosts[0].created.strftime('%Y-%m-%d %H:%M:%S')
        host['status'] = hosts[0].status
        # Cluster
        clusters = cluster_dao.getVOfromKey(uuid=hosts[0].cluster_uuid)
        host['cluster_name'] = clusters[0].name
        # Zone
        zones = zone_dao.getVOfromKey(uuid=clusters[0].zone_uuid)
        host['zone_name'] = zones[0].name
        # Region
        regions = region_dao.getVOfromKey(uuid=zones[0].region_uuid)
        host['region_name'] = regions[0].name


        return host
        #return self.locator.getInfo('HostInfo', hosts[0])

    ################################################################
    # Discover Host
    ################################################################
    def discoverHost(self, host_id):
        distro = self.detect_distro(host_id)
        # Update host DB
        host_dao = self.locator.getDAO('host')
        dic = {'status':'discovered'}
        host = host_dao.update(host_id, dic, 'uuid')

        return distro
 
    def connect(self, host_id):
        host_dao = self.locator.getDAO('host')
        hosts = host_dao.getVOfromKey(uuid=host_id)
        if hosts.count() == 0:
            raise ERROR_NOT_FOUND(key='host_id', value=host_id)
        host = hosts[0]
        ip = host.ipv4
        port = 22
        user_id = host.user_id
        passwd = host.password
        id_rsa = host.id_rsa
        id_dsa = host.id_dsa

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if passwd != '':
                    client.connect(ip, port, user_id, passwd,timeout=10)
            elif id_rsa != '':
                    pkeyfile = paramiko.RSAKey.from_private_key(StringIO.StringIO(id_rsa))
                    client.connect(ip, port, user_id, pkey=pkeyfile, timeout=10)
            elif id_dsa != '':
                    pkeyfile = paramiko.DSSKey.from_private_key(StringIO.StringIO(id_dsa))
                    client.connect(ip, port, user_id, pkey=pkeyfile, timeout=10)
            return client
        except:
            return None

    # execute commands with/out sudo
    # cmds : list of commands
    # return: output of command
    #           None, if failed
    def exec_cmd(self, host_id, cmds, sudo=False):
        output = []
        client = self.connect(host_id)
        if client == None:
            return None
        for cmd in cmds:
                if sudo == True:
                        new_cmd = "sudo %s" % cmd
                else:
                        new_cmd = cmd
                print new_cmd
                stdin, stdout, stderr = client.exec_command(new_cmd)
                output.append(stdout.readlines())
        client.close()
        return output

    def detect_distro(self, host_id):
            dist= "python -c 'import platform;print platform.linux_distribution()'"
            distro = self.exec_cmd(host_id, [dist])[0]
            msg = distro[0][1:-2].encode('ascii','ignore')
            items = msg.split(",")
            result = {"distname":items[0].split("'")[1],
                    "ver":items[1].split("'")[1],
                    "id":items[2].split("'")[1]}
            return result

