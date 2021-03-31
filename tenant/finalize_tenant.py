import logging

import config
import db
import sfdc

from tenant import jira, zendesk

def finalize(tenant_id: str, admin_email: str, password: str):
    if config.SymphonyTenantConfig['finalize_enabled']:

        logging.info(f"Tenant {tenant_id} complete!")
        tenant = db.get_tenant_by_admin_email(admin_email)

        if tenant:
            db_id = tenant['_id']
            db.update_tenant_status_by_id(db_id=db_id, status='complete')

            ssentry_id = tenant['ssentry_id']

            soql = f"SELECT Id, Account__c, POD__c FROM Self_Service_Entry__c WHERE Id = '{ssentry_id}' LIMIT 1"
            ssentry = sfdc.SalesforceClient.client.query(soql)['records'][0]

            # log_jiras(tenant, ssentry, tenant_id, admin_email, password)
            log_jiras_test(tenant, ssentry, tenant_id, admin_email, password)

            log_zendesk_tickets_test(tenant_id, ssentry, tenant_id, admin_email)

            sfdc.report_status_complete(ssentry_id=ssentry_id)
        else:
            details = f"{tenant_id}, {admin_email}, {password}"
            sfdc.report_generic_error('Unable to retrieve in-progress tenant from database.', details)

    else:
        logging.info('Finalize tenant skipped. Finalize disabled in config.')


def log_zendesk_tickets_test(db_tenant, ssentry, tenant_id: str, admin_email: str):
    ssentry_id = db_tenant['ssentry_id']
    company_name = db_tenant['company_name']
    admin_firstname = db_tenant['firstname']
    admin_lastname = db_tenant['lastname']

    account_id = ssentry['Account__c']
    tenant_url = f'https://{tenant_id}.p.symphony.com'

    # zendesk.create_client_ticket(company_name, tenant_url)

    org_id = zendesk.create_client_org(company_name, admin_email, tenant_url)
    zendesk.create_client_user(org_id, admin_firstname, admin_lastname, admin_email)

def log_jiras_test(db_tenant, ssentry, tenant_id: str, admin_email: str, password: str):
    ssentry_id = db_tenant['ssentry_id']
    company_name = db_tenant['company_name']
    admin_firstname = db_tenant['firstname']
    admin_lastname = db_tenant['lastname']

    reporter_id = config.JIRAConfig['reporter_id']
    account_id = ssentry['Account__c']
    tenant_url = f'https://{tenant_id}.p.symphony.com'

    customer_issue_fields = {
        'project': {'key': 'BIZOPS'},
        'summary': f'TEST ISSUE {company_name}',
        'issuetype': {'name': 'Task'},
        'reporter': {'id': reporter_id},
        # 'customfield_13300': f'https://symphony--c.na74.visual.force.com/apex/ConfigGateway?aid={account_id}',
        # 'components': [{'name': 'Customer Meeting'}],
    }

    customer_issue = jira.client.create_issue(fields=customer_issue_fields)

    # No reporter field on this issue
    config_issue_fields = {
        'project': {'key': 'BIZOPS'},
        'summary': tenant_url,
        'issuetype': {'name': 'Task'},
        'reporter': {'id': reporter_id}
        # 'customfield_15191': {'id': '13249'}
    }

    config_issue = jira.client.create_issue(fields=config_issue_fields)

    jira.client.create_issue_link('Problem/Incident', config_issue.key, customer_issue.key)



def log_jiras(db_tenant, ssentry, tenant_id: str, admin_email: str, password: str):
    ssentry_id = db_tenant['ssentry_id']
    company_name = db_tenant['company_name']
    admin_firstname = db_tenant['firstname']
    admin_lastname = db_tenant['lastname']

    reporter_id = config.JIRAConfig['reporter_id']
    account_id = ssentry['Account__c']
    tenant_url = f'https://{tenant_id}.p.symphony.com'

    # SA project_id = '15900

    customer_issue_fields = {
        'project': {'key': 'SA'},
        'summary': company_name,
        'issuetype': {'name': 'Customer'},
        'reporter': {'id': reporter_id},
        'customfield_13300': f'https://symphony--c.na74.visual.force.com/apex/ConfigGateway?aid={account_id}',
        'components': [{'name': 'Customer Meeting'}],
    }

    customer_issue = jira.client.create_issue(fields=customer_issue_fields)

    # No reporter field on this issue
    config_issue_fields = {
        'project': {'key': 'SA'},
        'summary': tenant_url,
        'issuetype': {'name': 'Pod'},
        'customfield_15191': {'id': '13249'}
    }

    config_issue = jira.client.create_issue(fields=config_issue_fields)

    jira.client.create_issue_link('Problem/Incident', config_issue.key, customer_issue.key)


