import dns
import logging
import pymongo

from . import BuildStatus

import config

class MongoClient:
    def __init__(self, username: str, password: str, database_name: str):
        self.conn_str = f"mongodb+srv://{username}:{password}@sym-bizops-mc.i40az.mongodb.net/{database_name}?" \
                        f"retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(self.conn_str)
        self.database_name = database_name

        self.tenant_id_collection_name = "tenant_ids"

    @staticmethod
    def from_config():
        uname = config.DatabaseConfig['username']
        pword = config.DatabaseConfig['password']
        db_name = config.DatabaseConfig['db_name']

        return MongoClient(username=uname, password=pword, database_name=db_name)

    def test_conn(self):
        try:
            logging.info('Testing Mongo Atlas connection...')
            db = self.client.test

            if not db:
                raise Exception('Mongo connection test failed.')
        except Exception as ex:
            logging.error(ex)

    def get_collection(self, collection_name: str):
        db = self.client.get_database(self.database_name)
        return db.get_collection(self.tenant_id_collection_name)

    def get_tenant_status(self, tenant_id: str):
        return self.get_collection(self.tenant_id_collection_name).find_one(
            {
                "tenant_id": {
                    "$eq": tenant_id
                }
            }
        )

    def get_pending_tenants(self):
        return self.get_collection(self.tenant_id_collection_name).find(
            {
                "$or": [
                    {"status": 'Pending'},
                    {"status": 'InProgress'}
                ]
            }
        )

    def insert_new_tenant(self, tenant_id: str):
        self.insert_tenant_status(tenant_id)

    def insert_tenant_status(self, tenant_id: str, status: BuildStatus=BuildStatus.Pending):
        self.get_collection(self.tenant_id_collection_name).insert_one(
            {
                "tenant_id": tenant_id,
                "status": status.name
            }
        )

    def update_tenant_status(self, tenant_id: str, status: BuildStatus):
        self.get_collection(self.tenant_id_collection_name).find_one_and_update(
            {
                "tenant_id": tenant_id
            },
            {
                "$set": {
                    "status": status.name
                }
            }
        )

    def delete_tenant_status(self, tenant_id: str):
        self.get_collection(self.tenant_id_collection_name).delete_one({"tenant_id": tenant_id})