
class Tenant:
    def __init__(self):
        self.shortname = ''
        self.vanityname = ''
        self.subdomain = ''

class TenantEvent:
    def __init__(self, event_message):
        self.tenant_id: str = event_message.get('Tenant_Id__c', '')
        self.ssentry_id: str = event_message['SSEntry_Id__c']
        self.type: str = event_message['Event_Type__c']
        self.auth_code: str = event_message['Event_Auth_Code__c']


# class TenantCreateEvent(TenantEvent):
#     def __init__(self, event_message):
#         super().__init__(event_message)
#
#         self.short_name: str = event_message.get('Short_Name__c', '')
#         self.vanity_name: str = event_message.get('Vanity_Name__c', '')
#         self.sub_domain: str = event_message.get('Sub_Domain__c', '')
#
#
# class TenantDeleteEvent(TenantEvent):
#     def __init__(self, event_message):
#         super().__init__(event_message)
#
#
# class TenantStatusCheck(TenantEvent):
#     def __init__(self, event_message):
#         super().__init__(event_message)