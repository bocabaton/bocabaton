from django.contrib.auth.hashers import make_password
from pyengine.lib import utils
from pyengine.lib import config
from pyengine.lib.error import *
from pyengine.manager import Manager 

import time
import paramiko
import pytz
import StringIO
from datetime import datetime

class WorkspaceManager(Manager):

    GLOBAL_CONF = config.getGlobalConfig()

    ########################################
    # CreateXXX
    ########################################
    def createWorkspace(self, params):
        ws_dao = self.locator.getDAO('workspace') 

        # TODO: check exist (user_id + name)

        dic = {}
        dic['user_id'] = params['user_id']
        dic['name'] = params['name']

        ws = ws_dao.insert(dic)

        # Update ws2user
        ws2user_dao = self.locator.getDAO('ws2user')
        if params.has_key('owner'):
            owners = params['owner']
            for owner in owners:
                dic2 = {}
                dic2['workspace_uuid'] = ws.uuid
                dic2['email'] = owner
                dic2['role'] = 'owner'
                ws2user = ws2user_dao.insert(dic2)

        # else, failed to create request
        # Disable workspace status 
        return self.locator.getInfo('WorkspaceInfo', ws)

    def createWorkflow(self, params):
        wf_dao = self.locator.getDAO('workflow') 


        dic = {}
        dic['workspace_uuid'] = params['workspace_id']
        dic['name'] = params['name']

        wf = wf_dao.insert(dic)

        return self.locator.getInfo('WorkflowInfo', wf)

    def deployWorkflow(self, params):
        wf_dao = self.locator.getDAO('workflow') 

        if params.has_key('workflow_id'):
            wfs = wf_dao.getVOfromKey(uuid=params['workflow_id'])
            if wfs.count() == 0:
                raise ERROR_NOT_FOUND(key='workflow_id', value=params['workflow_id'])
            #TODO: check user_id, workspace_id

        else:
            raise ERROR_REQUIRED_PARAM(key='workflow_id')

        ws_dao = self.locator.getDAO('workspace')
        wss = ws_dao.getVOfromKey(uuid=params['workspace_id'])
        if wss.count() == 0:
            raise ERROR_NOT_FOUND(key="workspace_id", value=params['workspace_id'])

        workspace_name = wss[0].name
        ######################################
        # TODO:
        # Singularity Manager
        # This code is for DEMO
        ######################################
        # Create Singularity request
        # TODO: update request parameter
        name1 = "%s_gerrit" % workspace_name
        sg_mgr = self.locator.getManager('SingularityManager')
        req = {
            "id": name1,
            "daemon": True,
            "rackSensitive": False,
            "loadBalanced": False
        }
        sg_mgr.createRequest(req)
        # If success

        # singularity deploy
        # Create Git
        d_git = {
            "deploy": {
            "requestId": name1,
            "id": "gerrit",
            "env": {"GERRIT_IP":"10.240.0.3"},
            "containerInfo": {
                "type": "DOCKER",
                "docker": {
                    "network": "HOST",
                    "image": "jhyoo/gerrit-boca:latest"
                    #"portMappings": [
                    #    {
                    #        "containerPort": 8080,
                    #        "hostPort": 8080,
                    #        "protocol": "tcp"
                    #    },
                    #    {
                    #        "containerPort": 29418,
                    #        "hostPort": 29418,
                    #        "protocol": "tcp"
                    #    }
                    #]
                }
            },
            "resources": {
                "cpus": 0.1,
                "memoryMb": 512
            },
            "skipHealthchecksOnDeploy": True
            }
        }
        result1 = sg_mgr.deployTask(d_git)
        # Update task information
        self.logger.info("Singularity Output:%s" % result1)

        for i in range(10):
            waiting = sg_mgr.checkPending()
            self.logger.info("Singularity waiting:%s" % waiting)
            if len(waiting) == 0:
                break
            time.sleep(2)

        # Create Jenkins
        name2 = "%s_jenkins" % workspace_name
        req = {
            "id": name2,
            "daemon": True,
            "rackSensitive": False,
            "loadBalanced": False
        }
        sg_mgr.createRequest(req)

 
        d_jenkins = {
            "deploy": {
            "requestId": name2,
            "id": "jenkins",
            "env": {"GERRIT_IP":"10.240.0.3"},
            "containerInfo": {
                "type": "DOCKER",
                "docker": {
                    "network": "BRIDGE",
                    #"image": "jenkins:latest",
                    "image": "jhyoo/jenkins-boca:dev-0.5",
                    "privileged": True,
                    "portMappings": [
                        {
                            "containerPortType": "LITERAL",
                            "containerPort": 8080,
                            "hostPortType": "FROM_OFFER",
                            "hostPort": 0,
                            "protocol": "tcp"
                        },
                        {
                            "containerPortType": "LITERAL",
                            "containerPort": 50000,
                            "hostPortType": "FROM_OFFER",
                            "hostPort": 1,
                            "protocol": "tcp"
                        }
                    ]
              }
            },
            "resources": {
                "cpus": 0.1,
                "memoryMb": 512,
                "numPorts": 2
            },
            "skipHealthchecksOnDeploy": True
            }
        }
 
        time.sleep(5)
        result2 = sg_mgr.deployTask(d_jenkins)
        # Update task information
        self.logger.info("Singularity Output:%s" % result2)


        return self.locator.getInfo('WorkflowInfo', wfs[0])



    #####################################################
    # Workflow/Task
    # params['deploy'] =
    # { "name" : "Git + Gerrit",
    #   "framework" : "singularity",
    #   "endpoint" : "127.0.0.1",
    #   "config" :
    #       {
    #        "deploy": {
    #            "requestId": "{put your workspace name}",
    #            "id": "git+gerrit",
    #            "containerInfo": {
    #                "type": "DOCKER",
    #                "docker": {
    #                    "network": "BRIDGE",
    #                    "image": "bocabaton/git:latest",
    #                    "portMappings": [
    #                        {
    #                            "containerPortType": "LITERAL",
    #                            "containerPort": 80,
    #                            "hostPortType": "FROM_OFFER",
    #                            "hostPort": 0,
    #                            "protocol": "tcp"
    #                        }
    #                    ]
    #                }
    #            },
    #            "resources": {
    #                "cpus": 0.1,
    #                "memoryMb": 256,
    #                "numPorts": 1
    #            },
    #            "skipHealthchecksOnDeploy": True,
    #            "healthcheckUri": "/healthcheck"
    #        }
    #        }
    # }
    #####################################################
    def deployBpmnTask(self, params):

        sg_mgr = self.locator.getManager('SingularityManager')
        # create sigularity request
        request_name = params['deploy']['config']['deploy']['requestId']
        endpoint = params['deploy']['endpoint']
        req = {
            "id": request_name,
            "daemon": True,
            "rackSensitive": False,
            "loadBalanced": False
        }
        sg_mgr.createRequest(req, endpoint='127.0.0.1')
   
        config = params['deploy']['config']
        result = sg_mgr.deployTask(config, endpoint)  

        # deploy container
    
        return {"success":True}

    ################################################
    # ListXXX
    ################################################
    def listWorkspaces(self, search, sort, page, res_params):
        ws_dao = self.locator.getDAO('workspace')

        output = []
        (wss, total_count) = ws_dao.select(search=search, sort=sort, page=page)

        for ws in wss:
            ws_info = self.locator.getInfo('WorkspaceInfo', ws, res_params=res_params)
            output.append(ws_info)

        return (output, total_count)


    ####################################################
    # getXXX
    ####################################################
    def getWorkspace(self, params):
        ws_dao = self.locator.getDAO('workspace')

        if params.has_key('name'):
            wss = ws_dao.getVOfromKey(name=params['name'])
            if wss.count() == 0:
                raise ERROR_NOT_FOUND(key='name', value=params['name'])

        else:
            raise ERROR_REQUIRED_PARAM(key='name')

        return self.locator.getInfo('WorkspaceInfo', wss[0])

    #####################################################
    # Workflow/Task
    # params['add'] =
    # { "name" : "Git + Gerrit",
    #   "fw_type" : "singularity",
    #   "category" : "DevOps",
    #   "config" :
    #       {
    #        "deploy": {
    #            "requestId": "{put your workspace name}",
    #            "id": "git+gerrit",
    #            "containerInfo": {
    #                "type": "DOCKER",
    #                "docker": {
    #                    "network": "BRIDGE",
    #                    "image": "bocabaton/git:latest",
    #                    "portMappings": [
    #                        {
    #                            "containerPortType": "LITERAL",
    #                            "containerPort": 80,
    #                            "hostPortType": "FROM_OFFER",
    #                            "hostPort": 0,
    #                            "protocol": "tcp"
    #                        }
    #                    ]
    #                }
    #            },
    #            "resources": {
    #                "cpus": 0.1,
    #                "memoryMb": 256,
    #                "numPorts": 1
    #            },
    #            "skipHealthchecksOnDeploy": True,
    #            "healthcheckUri": "/healthcheck"
    #        }
    #        }
    # }
    #####################################################

    def addWorkflowTask(self, params):
        wft_dao = self.locator.getDAO('task_template')

        p = params['add']
        dic = {}
        dic['name']     = p['name']
        dic['fw_type']  = p['fw_type']
        dic['category'] = p['category']
        # param is dictionary
        # save as json content
        dic['config']   = json.dumps(p['config'])

        wft = wft_dao.insert(dic)

        return self.locator.getInfo('WorkflowTaskInfo', wft)

    def getWorkflowTask(self, params):
        wft_dao = self.locator.getDAO('task_template')

        wfts = wft_dao.getVOfromKey(name=params['get']['name'])
        if wfts.count() == 0:
            raise ERROR_NOT_FOUND(key='name', value=params['get']['name'])
        return self.locator.getInfo('WorkflowTaskInfo', wfts[0])

