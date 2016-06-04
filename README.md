# BocaBaton

BocaBaton is Container Automation System

# To make demo

You can easily build BocaBaton with Mesos/Singularity.

## CentOS

To build BocaBaton in CentOS

~~~python
yum install -y epel-release
yum install -y python-pip
pip install jeju --upgrade

jeju -m https://raw.githubusercontent.com/bocabaton/bocabaton/master/docs/INSTALL_CentOS.md
~~~

The Demo Web
-> http://<your ip>/admin/

## Vagrant

### Prerequisites
=======

Install VirtualBox/Vmware and Vagrant (version 1.8 or above)

To use virtualbox:
```bash
git clone https://github.com/bocabaton/bocabaton.git
export VAGRANT_DEFAULT_PROVIDER="virtualbox"
vagrant up
```

To use vmware fusion:
```bash
git clone https://github.com/bocabaton/bocabaton.git
export VAGRANT_DEFAULT_PROVIDER="vmware_fusion"
vagrant up
```

To use vmware workstation:
```bash
git clone https://github.com/bocabaton/bocabaton.git
export VAGRANT_DEFAULT_PROVIDER="vmware_workstation"
vagrant up
```

Installation takes about 15 min, depending on your internet connection.

Once completed, open a browser and hit http://vagrant-bocabaton/admin/

# Powered by PyEngine
https://github.com/pyengine/pyengine.git
