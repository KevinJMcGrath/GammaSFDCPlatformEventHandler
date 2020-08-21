import config

from .apex_client import SFClient
from .events_client import EventsClient


PlatformEventsClient = EventsClient(config.SFDCPlatformConfig, heartbeat_delay=config.HeartbeatDelay)
SalesforceClient = SFClient(config.SFDCPlatformConfig)