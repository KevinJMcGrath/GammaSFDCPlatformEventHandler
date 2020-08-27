import jsonpickle
import os

from pathlib import Path

deploy_type = os.environ.get('DEPLOY_TYPE')

if deploy_type == 'prod':
    config_path = '/etc/public_housekeeper/bot_config/config.json'
else:
    config_path = Path("./config.json")

with open(config_path, 'r') as _config_file:
    _config = jsonpickle.decode(_config_file.read())

HeartbeatDelay = _config['heartbeat_delay']
SFDCPlatformConfig = _config['sfdc_platform']
SymphonyTenantConfig = _config['sym_tenant']
DatabaseConfig = _config['databse']


LogVerbose = _config['log_verbose']