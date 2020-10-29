import dns
import logging
import pymongo
import bson


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
            # logging.debug('Testing Mongo Atlas connection...')
            db = self.client.test

            if not db:
                raise Exception('Mongo connection test failed.')
        except Exception as ex:
            logging.error(ex)

            # If the database test fails, I want the script to bail out.
            raise ex

    def get_collection(self, collection_name: str):
        db = self.client.get_database(self.database_name)
        return db.get_collection(self.tenant_id_collection_name)

    def get_tenant_status_by_tenant_id(self, tenant_id: str):
        logging.debug(f"get_tenant_status tenant_id: {tenant_id}")
        return self.get_collection(self.tenant_id_collection_name).find_one(
            {
                "tenant_id": {
                    "$eq": tenant_id
                }
            }
        )

    def get_tenant_status_by_mt_event_id(self, mt_event_id: str):
        logging.debug(f"get_tenant_status mt_event_id: {mt_event_id}")
        return self.get_collection(self.tenant_id_collection_name).find_one(
            {
                "mt_event_id": {
                    "$eq": mt_event_id
                }
            }
        )

    def get_tenant_status_by_ssentry_id(self, ssentry_id: str):
        logging.debug(f"get_tenant_status_by_ssentry_id: {ssentry_id}")
        return self.get_collection(self.tenant_id_collection_name).find_one(
            {
                "ssentry_id": {
                    "$eq": ssentry_id
                }
            }
        )

    def get_tenant_status_by_admin_email(self, admin_email: str):
        logging.debug(f"get_tenant_status_by_admin_email: {admin_email}")
        return self.get_collection(self.tenant_id_collection_name).find_one(
            {
                "admin_email": {
                    "$eq": admin_email
                }
            }
        )

    def get_pending_tenants(self):
        return self.get_collection(self.tenant_id_collection_name).find(
            {
                "$or": [
                    {"status": 'submitted'},
                    {"status": 'in_progress'}
                ]
            }
        )

    def insert_new_tenant(self, ssentry_id: str, tenant_id: str=None, mt_event_id: str=None, admin_email: str=None,
                          company_name: str=None, admin_fname: str=None, admin_lname: str=None):

        logging.debug(f"insert_new_tenant ssentry_id: {ssentry_id}")

        self.insert_tenant_status(tenant_id=tenant_id, ssentry_id=ssentry_id, status='submitted',
                                  mt_event_id=mt_event_id, admin_email=admin_email, company_name=company_name,
                                  admin_fname=admin_fname, admin_lname=admin_lname)

    def insert_tenant_status(self, tenant_id: str, ssentry_id: str, status: str, mt_event_id: str=None,
                             admin_email: str=None, company_name: str=None, admin_fname: str=None, admin_lname: str=None):
        logging.debug(f"insert_tenant_status admin_email: {admin_email} - ssentry_id: {ssentry_id} - status: {status}")
        self.get_collection(self.tenant_id_collection_name).insert_one(
            {
                "tenant_id": tenant_id,
                "ssentry_id": ssentry_id,
                "status": status,
                "mt_event_id": mt_event_id,
                "admin_email": admin_email,
                "company_name": company_name,
                "firstname": admin_fname,
                "lastname": admin_lname
            }
        )

    def update_tenant_status_by_tenant_id(self, tenant_id: str, status: str):
        logging.debug(f"update_tenant_status tenant_id: {tenant_id} - status: {status}")
        self.get_collection(self.tenant_id_collection_name).find_one_and_update(
            {
                "tenant_id": tenant_id
            },
            {
                "$set": {
                    "status": status
                }
            }
        )

    def update_tenant_status_by_ssentry_id(self, ssentry_id: str, status: str):
        logging.debug(f"update_tenant_status tenant_id: {ssentry_id} - status: {status}")
        self.get_collection(self.tenant_id_collection_name).find_one_and_update(
            {
                "ssentry_id": ssentry_id
            },
            {
                "$set": {
                    "status": status
                }
            }
        )

    def update_tenant_status_by_id(self, db_id, status: str):
        logging.debug(f"update_tenant_status _id: {db_id} - status: {status}")
        self.get_collection(self.tenant_id_collection_name).update_one(
            {
                "_id": bson.ObjectId(db_id)
            },
            {
                "$set": {
                    "status": status
                }
            }
        )

    def update_tenant_event_id_by_ssentry_id(self, ssentry_id: str, mt_event_id: str):
        logging.debug(f"update_tenant_event_id_by_ssentry_id ssentry_id: {ssentry_id} - mt_event_id: {mt_event_id}")
        self.get_collection(self.tenant_id_collection_name).update_one(
            {
                "ssentry_id": ssentry_id
            },
            {
                "$set": {
                    "mt_event_id": mt_event_id
                }
            }
        )

    def delete_tenant_status_by_tenant_id(self, tenant_id: str):
        self.get_collection(self.tenant_id_collection_name).delete_one({"tenant_id": tenant_id})

    def delete_tenant_status_by_ssentry_id(self, ssentry_id: str):
        self.get_collection(self.tenant_id_collection_name).delete_one({"ssentry_id": ssentry_id})