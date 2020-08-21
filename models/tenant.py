from dataclasses import dataclass

class Tenant:
    def __init__(self):
        self.shortname = ''
        self.vanityname = ''
        self.subdomain = ''


class TenantCreateEvent:
    def __init__(self, event_message):
        self.ssentry_id: str = event_message['SSEntry_Id__c']
        self.short_name: str = event_message.get('Short_Name__c', '')
        self.vanity_name: str = event_message.get('Vanity_Name__c', '')
        self.sub_domain: str = event_message.get('Sub_Domain__c', '')
        self.tenant_id: str = event_message.get('Tenant_Id__c', '')