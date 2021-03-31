from zenpy import Zenpy
from zenpy.lib.api_objects import User

import config

class ZenClient:
    def __init__(self):
        self.client: Zenpy = Zenpy(**config.ZendeskConfig)


    def create_client_ticket(self, company_name, tenant_url):
        subject = f'New Self Service Client: {company_name}'
        comment = { 'body': f'Tenant URL: {tenant_url}'}
        assignee_email = 'kevin.mcgrath@symphony.com'

        ticket = self.client.tickets.create(subject=subject, comment=comment, assignee_email=assignee_email)

    def create_client_org(self, company_name: str, admin_email: str, tenant_url: str):

        company_domain_list = [admin_email.split('@')[1]]
        notes = f'Self-Service Client \n Tenant URL: {tenant_url}'
        tags = ['gamma', 'business']

        resp = self.client.organizations.create(name=company_name, domain_names=company_domain_list, notes=notes,
                                                tags=tags)
        org_id = resp['organization']['id']

        return org_id

    def create_client_user(self, org_id: str, user_first_name: str, user_last_name: str, user_email: str):
        user_fullname = f'{user_first_name} {user_first_name}'

        user = User(name=user_fullname, email=user_email, organization_id=org_id, verified=True, notes='Gamma User')


        resp = self.client.end_user.create(user)