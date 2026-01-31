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
