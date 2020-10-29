import logging

from datetime import datetime
from jira import JIRA

import config
import db
import sfdc

def finalize(tenant_id: str, admin_email: str, password: str):
    logging.info(f"Tenant ({tenant_id} complete!")

    tenant = db.get_tenant_by_admin_email(admin_email)
    db_id = tenant['_id']
    ssentry_id = tenant['ssentry_id']

    db.update_tenant_status_by_id(db_id=db_id, status='complete')

    soql = f"SELECT Id, Account__c, POD__c, Symphony_URL__c FROM Self_Service_Entry__c WHERE Id = '{ssentry_id}' LIMIT 1"
    ssentry = sfdc.SalesforceClient.client.query(soql)['records'][0]

    log_jiras(tenant, ssentry, tenant_id, admin_email, password)

    sfdc.report_status_complete(ssentry_id=ssentry_id)


def log_jiras(db_tenant, ssentry, tenant_id: str, admin_email: str, password: str):
    ssentry_id = db_tenant['ssentry_id']
    company_name = db_tenant['company_name']
    admin_firstname = db_tenant['firstname']
    admin_lastname = db_tenant['lastname']

    server = config.JIRAConfig['server']
    uname = config.JIRAConfig['username']
    token = config.JIRAConfig['api_token']

    reporter_id = config.JIRAConfig['reporter_id']
    account_id = ssentry_id['Account__c']
    tenant_url = f'https://{tenant_id}.p.symphony.com'

    j = JIRA(server=server, basic_auth=(uname, token))

    customer_issue_fields = {
        'project': {'key': 'SA'},
        'summary': company_name,
        'issuetype': {'name': 'Customer'},
        'reporter': {'id': reporter_id},
        'customfield_13300': f'https://symphony--c.na74.visual.force.com/apex/ConfigGateway?aid={account_id}',
        'components': [{'name': 'Customer Meeting'}],
    }

    customer_issue = j.create_issue(fields=customer_issue_fields)

    # No reporter field on this issue
    config_issue_fields = {
        'project': {'key': 'SA'},
        'summary': tenant_url,
        'issuetype': {'name': 'Pod'},
        'customfield_15191': {'id': '13249'}
    }

    config_issue = j.create_issue(fields=config_issue_fields)

    j.create_issue_link('Problem/Incident', config_issue.key, customer_issue.key)


