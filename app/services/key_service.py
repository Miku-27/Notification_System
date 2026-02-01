from hashlib import sha256
from secrets import token_urlsafe,compare_digest
from app.models.model import ApikeyTable

def _generate_api_key():
    return token_urlsafe(32)

def _hash_api_key(plain_key):
    return sha256(plain_key.encode()).hexdigest()

def verify_api_key(db,key_name,key):
    hashed_key =  _hash_api_key(plain_key=key)

    record = db.query(ApikeyTable).filter(ApikeyTable.apikey_name == key_name).first()
    if not record:
        return False

    hashed_key = _hash_api_key(key)
    return record.id if compare_digest(record.apikey_hash,hashed_key) else None

def add_project(db,project_dict):
    try:
        project = db.query(ApikeyTable.id).filter(ApikeyTable.apikey_name == project_dict['project_name']).first()
        if project:
            return False
        
        api_key = _hash_api_key(_generate_api_key())
        project = ApikeyTable(
            apikey_name = project_dict['project_name'],
            apikey_hash = api_key
        )

        db.add(project)
        db.commit() 
        return True
    
    except Exception as e:
        db.rollback()
        print(e)
        return False

def remove_project(db,project_dict):
    try:
        project = db.query(ApikeyTable.id).filter(ApikeyTable.apikey_name == project_dict['project_name']).first()
        if not project:
            return False
        
        db.delete(project)
        db.commit() 
        return True
    
    except Exception as e:
        db.rollback()
        print(e)
        return False
    
def generate_new_apiKey(db,project_dict):
    try:
        project = db.query(ApikeyTable.id).filter(ApikeyTable.apikey_name == project_dict['project_name']).first()
        if not project:
            return False
        
        api_key = _hash_api_key(_generate_api_key())
        project = ApikeyTable(
            apikey_name = project_dict['project_name'],
            apikey_hash = api_key
        )
        db.commit() 
        return True
    
    except Exception as e:
        db.rollback()
        print(e)
        return False