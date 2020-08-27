
# https://aiosfstream.readthedocs.io/en/latest/quickstart.html
from aiosfstream import SalesforceStreamingClient

class EventsClient:
    def __init__(self, platform_config):
        self.client_key = platform_config['client_key']
        self.client_secret = platform_config['client_secret']
        self.username = platform_config['username']
        self.password = platform_config['password']
        self.security_token = platform_config['security_token']
        self.sandbox = platform_config['sandbox']
        self.channel = platform_config['event_channel']

        self.client: SalesforceStreamingClient = self.init_client()

    # Create Platform Event
    # Endpoint: /services/data/v48.0/sobjects/Tenant_Event__e
    # https://developer.salesforce.com/docs/atlas.en-us.226.0.platform_events.meta/platform_events/platform_events_publish_api.htm
    def init_client(self):
        return SalesforceStreamingClient(consumer_key=self.client_key, consumer_secret=self.client_secret,
                                    username=self.username, password=self.password + self.security_token,
                                    sandbox=self.sandbox)