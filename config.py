import jsonpickle
import os

from pathlib import Path

deploy_type = os.environ.get('DEPLOY_TYPE')

if deploy_type == 'prod':
    config_path = '/etc/gamma-tenant-manager/config/config.json'
else:
    config_path = Path("config/config.json")

with open(config_path, 'r') as _config_file:
    _config = jsonpickle.decode(_config_file.read())

HeartbeatDelay = _config['heartbeat_delay']
SFDCPlatformConfig = _config['sfdc_platform']
SymphonyTenantConfig = _config['sym_tenant']
DatabaseConfig = _config['databse']
BotConfig = _config['bot']
JIRAConfig = _config['jira']
ZendeskConfig = _config['zendesk']


LogVerbose = _config['log_verbose']
AppVersion = _config['app_version']