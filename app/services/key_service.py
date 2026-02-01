from hashlib import sha256
from secrets import token_urlsafe,compare_digest
from app.models.model import ApikeyTable
from app.utils.response import ResultCodes

def _generate_api_key():
    return token_urlsafe(32)

def _hash_api_key(plain_key):
    return sha256(plain_key.encode()).hexdigest()

def verify_api_key(db,key_name,key):
    hashed_key =  _hash_api_key(plain_key=key)

    record = db.query(ApikeyTable).filter(ApikeyTable.apikey_name == key_name).first()
    if not record:
        return {
            'success':False,
            'code':True
        }

    hashed_key = _hash_api_key(key)
    is_verified = True if compare_digest(record.apikey_hash,hashed_key) else None
    if is_verified:
        return {
            'success':True,
            'code':ResultCodes.IDENTITY_VERIFIED,
            'data': record.id
        }
    else:
        return {
            'success':False,
            'code':ResultCodes.IDENTITY_INVALID,
            'data': None
        }

def add_indentity(db,indentity_dict):
    try:
        indentity = db.query(ApikeyTable.id).filter(ApikeyTable.apikey_name == indentity_dict['indentity_name']).first()
        if indentity:
            return {
                'success':False,
                'code':ResultCodes.IDENTITY_ALREADY_EXIST
            }
        
        api_key = _hash_api_key(_generate_api_key())
        indentity = ApikeyTable(
            apikey_name = indentity_dict['indentity_name'],
            apikey_hash = api_key
        )

        db.add(indentity)
        db.commit() 
        return {
            'success':True,
            'code':ResultCodes.IDENTITY_CREATED
        }
    
    except Exception as e:
        db.rollback()
        print(e)
        return {
            'success':False,
            'code':ResultCodes.INTERNAL_SERVER_ERROR
        }

def remove_indentity(db,indentity_dict):
    try:
        indentity = db.query(ApikeyTable.id).filter(ApikeyTable.apikey_name == indentity_dict['indentity_name']).first()
        if not indentity:
            return {
                'success':False,
                'code':ResultCodes.IDENTITY_NOT_FOUND
            }
        
        db.delete(indentity)
        db.commit() 
        return {
            'success':True,
            'code':ResultCodes.IDENTITY_DELETED
        }
    
    except Exception as e:
        db.rollback()
        print(e)
        return {
            'success':False,
            'code':ResultCodes.INTERNAL_SERVER_ERROR
        }
    
def generate_new_apiKey(db,indentity_dict):
    try:
        indentity = db.query(ApikeyTable.id).filter(ApikeyTable.apikey_name == indentity_dict['indentity_name']).first()
        if not indentity:
            return {
                'success':False,
                'code':ResultCodes.IDENTITY_NOT_FOUND
            }
        
        api_key = _hash_api_key(_generate_api_key())
        indentity = ApikeyTable(
            apikey_name = indentity_dict['indentity_name'],
            apikey_hash = api_key
        )
        db.commit() 
        return {
            'success':True,
            'code':ResultCodes.IDENTITY_UPDATED
        }
    
    except Exception as e:
        db.rollback()
        print(e)
        return {
            'success':False,
            'code':ResultCodes.INTERNAL_SERVER_ERROR
        }