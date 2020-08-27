import config

from .apex_client import SFClient
from .events_client import EventsClient


PlatformEventsClient = EventsClient(config.SFDCPlatformConfig)
SalesforceClient = SFClient(config.SFDCPlatformConfig)