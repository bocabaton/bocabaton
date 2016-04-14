from pyengine.lib import utils
from django.conf import settings

PYENGINE_CONF = getattr(settings, 'PYENGINE')

def getGlobalConfig(): 
    conf = utils.loadYAML(PYENGINE_CONF['global'])

    return conf['GLOBAL']

def getRouterConfig(): 
    conf = utils.loadYAML(PYENGINE_CONF['router'])

    return conf['ROUTER']

def getErrorConfig(): 
    conf = utils.loadYAML(PYENGINE_CONF['error'])

    return conf['ERROR']

def getPluginConfig(): 
    conf = utils.loadYAML(PYENGINE_CONF['plugin'])

    return conf['PLUGIN']
