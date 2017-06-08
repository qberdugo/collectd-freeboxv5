import collectd
import freebox_v5_status.freeboxstatus
import netaddr


PLUGIN_NAME = 'freeboxv5'
INTERVAL = 60  # seconds

_fbx = None

collectd.info('Loading Python plugin:' + PLUGIN_NAME)


def init():
    """
    Init of the freebox object
    """
    global _fbx
    collectd.info('Initialization :' + PLUGIN_NAME)
    _fbx = freebox_v5_status.freeboxstatus.FreeboxStatus()


def configure(config):
    """
    Read configuration options
    """
    for node in config.children:
        key = node.key.lower()
        val = node.values[0]

        if key == 'interval':
            global INTERVAL
            INTERVAL = val
        else:
            collectd.info('Freeboxv5 plugin: Unknown config key "%s"' % key)



def read(data=None):
    """
    Reads values from freebox and dispatches them to collectd
    """

    global _fbx
    _fbx.update()

    CRC_up = _fbx.status['adsl']['CRC']['up']
    CRC_down = _fbx.status['adsl']['CRC']['down']
    FEC_up = _fbx.status['adsl']['FEC']['up']
    FEC_down = _fbx.status['adsl']['FEC']['down']
    HEC_up = _fbx.status['adsl']['HEC']['up']
    HEC_down = _fbx.status['adsl']['HEC']['down']
    attenuation_up = _fbx.status['adsl']['attenuation']['up']
    attenuation_down = _fbx.status['adsl']['attenuation']['down']
    sync_up = _fbx.status['adsl']['synchro_speed']['up']
    sync_down = _fbx.status['adsl']['synchro_speed']['down']
    uptime = _fbx.status['general']['uptime'].total_seconds()
    publicIP = int(netaddr.IPAddress(_fbx.status['network']['public_ip']))

    dispatch_value('uptime', 'uptime', (uptime,))
    dispatch_value('ATM_errors', 'CRC', (CRC_down, CRC_up))
    dispatch_value('ATM_errors', 'FEC', (FEC_down, FEC_up))
    dispatch_value('ATM_errors', 'HEC', (HEC_down, HEC_up))
    dispatch_value('attenuation', 'attenuation', (attenuation_down, attenuation_up))
    dispatch_value('sync', 'sync', (sync_down, sync_up))
    dispatch_value('IP', 'public_ip', (publicIP,))


def dispatch_value(val_type, type_instance, value, plugin_instance=''):
    """
    Dispatch a value to collectd
    """
    collectd.info('Dispatching: %s=%r' % (type_instance, value))
    val = collectd.Values()
    val.plugin = PLUGIN_NAME
    val.plugin_instance = plugin_instance
    val.type = val_type
    if len(type_instance):
        val.type_instance = type_instance
    val.values = value
#    val.interval = 10
    val.dispatch()

#
# Register our callbacks to collectd
#

collectd.register_init(init)
collectd.register_config(configure)
collectd.register_read(read, INTERVAL)


