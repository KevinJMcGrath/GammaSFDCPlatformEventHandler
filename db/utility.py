from datetime import datetime

def get_created_datetime(db_item) -> datetime:
    return db_item.get('_id').generation_time