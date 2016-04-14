# Mesos Setup

# Environment

Keyword | Value
----    | -----
MYID    | 1
DEV     | eth0
SINGULARITY_VER | 0.4.7
REPO    | https://github.com/bocabaton/bocabaton.git

# Setup Mesos

~~~bash
rpm -Uvh http://repos.mesosphere.io/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm
~~~

# Installation

~~~bash
yum -y install net-tools
yum -y install mesos
yum -y install mesosphere-zookeeper
yum -y install docker
~~~

# Edit Zookeeper

## Update myid

myid must be unique on cluster

edit /var/lib/zookeeper/myid

~~~text
${MYID}
~~~

## Update zookeeper zoo.cfg

edit /etc/zookeeper/conf/zoo.cfg

~~~text
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

maxClientCnxns=50
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
dataDir=/var/lib/zookeeper
# the port at which the clients will connect
clientPort=2181
server.1=${IP}:2888:3888
~~~

## Restart Zookeeper

~~~bash
systemctl enable zookeeper.service
systemctl restart zookeeper.service
~~~

# Edit mesos

Update date zookeeper with proper IP

edit /etc/mesos/zk

~~~text
zk://${IP}:2181/mesos
~~~

## Update Quorum

edit /etc/mesos-master/quorum

~~~text
1
~~~

## Update memsos-master config

edit /etc/mesos-master/ip

~~~bash
hostname -i > /etc/mesos-master/ip
~~~

## Update mesos-slave config

edit /etc/mesos-slave/ip

~~~bash
hostname -i > /etc/mesos-slave/ip
~~~

## Update containerizers

edit /etc/mesos-slave/containerizers

~~~text
docker,mesos
~~~

We support docker

## Update registration timeout

timeout update

create /etc/mesos-slave/executor_registration_timeout

~~~bash
echo "5mins" > /etc/mesos-slave/executor_registration_timeout
~~~

## Restart mesos master

~~~bash
systemctl enable mesos-master.service
systemctl start mesos-master.service
systemctl enable mesos-slave.service
systemctl start mesos-slave.service
~~~

# Reference

https://mesosphere.com/downloads/


# Sigularity

## Get source

~~~bash
yum install -y wget
wget -O /usr/local/bin/SingularityService-${SINGULARITY_VER}-shaded.jar https://repo1.maven.org/maven2/com/hubspot/SingularityService/${SINGULARITY_VER}/SingularityService-${SINGULARITY_VER}-shaded.jar
~~~

# To run

## create sigularity configuration file

~~~bash
mkdir /etc/singularity/
~~~

## update configuration file

edit /etc/singularity/singularity.yaml

~~~text
# Run SingularityService on port 7099 and log to /var/log/singularity-access.log
server:
  type: simple
  applicationContextPath: /singularity
  connector:
    type: http
    port: 7099
  requestLog:
    appenders:
      - type: file
        currentLogFilename: /var/log/singularity-access.log
        archivedLogFilenamePattern: /var/log/singularity-access-%d.log.gz

mesos:
  master: zk://${IP}:2181/mesos
  defaultCpus: 1
  defaultMemory: 128
  frameworkName: Singularity
  frameworkId: Singularity
  frameworkFailoverTimeout: 1000000

zookeeper:
  quorum: ${IP}:2181
  zkNamespace: singularity
  sessionTimeoutMillis: 60000
  connectTimeoutMillis: 5000
  retryBaseSleepTimeMilliseconds: 1000
  retryMaxTries: 3

logging:
  loggers:
    "com.hubspot.singularity" : TRACE

enableCorsFilter: true
sandboxDefaultsToTaskId: false  # enable if using SingularityExecutor

ui:
  title: Singularity (lsky)
  baseUrl: http://${IP}:7099/singularity
~~~

## Create start script

edit /usr/lib/systemd/system/singularity.service

~~~text
[Unit]
Description=Singularity Master
After=network.target
Wants=network.target

[Service]
ExecStart=/usr/bin/java -jar /usr/local/bin/SingularityService-${SINGULARITY_VER}-shaded.jar server /etc/singularity/singularity.yaml
Restart=always
RestartSec=20
LimitNOFILE=16384

[Install]
WantedBy=multi-user.target
~~~

## Restart Singularity Service

~~~bash
systemctl enable singularity.service
systemctl start singularity.service
~~~

# Install at CentOS 7

## Download source

~~~bash
yum install -y git
cd /opt/
git clone ${REPO}
~~~

## Install Packages

~~~bash
yum install -y python-devel python-pip mariadb-server mariadb MySQL-python httpd mod_wsgi
~~~

## PIP package install

~~~bash
pip install django
pip install django-log-request-id
pip install dicttoxml
pip install xmltodict
pip install routes
pip install rsa
pip install pytz
pip install pyyaml
yum install -y python-paramiko
~~~


## Update Python module path environment
~~~bash
echo "/opt/bocabaton" > /usr/lib/python2.7/site-packages/pyengine.pth
~~~

# Update Apache configuration

edit /etc/httpd/conf.d/bocabaton.conf

~~~text
<VirtualHost *:80>
    Alias /admin/ /opt/bocabaton/admin/
    <Directory /opt/bocabaton/admin>
        Require all granted
    </Directory>

    WSGIScriptAlias / /opt/bocabaton/pyengine/wsgi.py
    WSGIPassAuthorization On

    <Directory /opt/bocabaton/pyengine>
    <Files wsgi.py>
        Require all granted
    </Files>
    </Directory>

    AddDefaultCharset UTF-8

</VirtualHost>
~~~

# Create database

~~~bash
systemctl enable mariadb.service
systemctl restart mariadb.service
mysql -uroot -e "create database pyengine character set utf8 collate utf8_general_ci"
~~~

# Update django

~~~bash
mkdir /var/log/pyengine
chown -R apache:apache /var/log/pyengine

cd /opt/bocabaton
python manage.py makemigrations
python manage.py migrate

~~~

# Restart apache

~~~bash
systemctl enable httpd.service
systemctl restart httpd.service
~~~

# Restart Apache

~~~bash
systemctl restart httpd.service
~~~

# Check BocaBaton Status


edit /root/jeju.log

~~~text
MESOS UI:           http://${IP}:5050
SINGULARITY API:        http://${IP}:7099
BocaBaton Control Center:   http://${IP}/admin/
BocaBaton API Server:       http://${IP}/api
~~~

# Make intial data

~~~python

import requests
import json

headers = {'Content-Type':'application/json'}

def makeRegion(region_name):
    req_body = {'name':region_name}
    url = 'http://127.0.0.1/api/v1/compute/regions'
    r = requests.post(url, headers=headers, data=json.dumps(req_body))
    result = json.loads(r.text)
    print r.text
    return result['region_id']


def makeZone(zone_name, region_id):
    req_body = {'name':zone_name, 'region_id':region_id}
    url = 'http://127.0.0.1/api/v1/compute/zones'
    r = requests.post(url, headers=headers, data=json.dumps(req_body))
    result = json.loads(r.text)
    return result['zone_id']

def makeCluster(cluster_name, zone_id):
    req_body = {'name':cluster_name, 'zone_id':zone_id} 
    url = 'http://127.0.0.1/api/v1/compute/clusters'
    r = requests.post(url, headers=headers, data=json.dumps(req_body))
    result = json.loads(r.text)
    return result['cluster_id']

def makeHost(name, domain, ipv4, user_id, password, cluster_id):
    req_body = {'name':name, 'domain':domain, 'ipv4':ipv4, 'user_id':user_id, 'password':password, 'cluster_id':cluster_id}
    url = 'http://127.0.0.1/api/v1/compute/hosts'
    r = requests.post(url, headers=headers, data=json.dumps(req_body))
    result = json.loads(r.text)
    return result['host_id']

r_id = makeRegion('Test Region #1')
z_id = makeZone('Test Zone #1', r_id)
c_id = makeCluster('Cluster #1', z_id)
h_id = makeHost('vm1','bocabaton.net','${IP}','root','123456',c_id)

~~~

