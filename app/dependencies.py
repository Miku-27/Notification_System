from fastapi import Header,Depends,HTTPException
from app.models.database import get_db
from app.services.auth_service import verify_api_key
from sqlalchemy.orm import Session

def validate_api_key(
        x_project_name:str = Header(...),
        x_api_key:str = Header(...),
        db :Session = Depends(get_db)
    ):
    project_id = verify_api_key(db,x_project_name,x_api_key) 

    if not project_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    return project_id 