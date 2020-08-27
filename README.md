# Gamma Tenant Manager

## Installation
TBD

## Startup:
On startup, an asyncio loop is created and the following tasks are gathered:
* Heartbeat generator
* Platform Event listener
* Platform Event queue processor
* Tenant build monitor

## Processing

### Submission:
1. SFDC emits a new Platform Event after Gamma Signup
2. PE is received by events_client listener
3. PE is processed and routed to platform event queue
4. PE is popped off PEQ and processed by relevant consumer

### Tenant Create Queue Consumer
1. Add tenant_id to database with status 'Pending'
2. POST to spinnaker create API
3. Process result
   1. Success
      1. Update database to status 'InProgress'
      2. POST to SFDC update API to status 'InProgress'
      3. Push tenant_id to Tenant Monitoring Queue
   2. Failure
      1. Update database to status 'Failed'
      2. POST to SFDC update API to status 'Failed'