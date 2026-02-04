from fastapi import APIRouter,Depends
from app.models.pydantic_models import identityModel
from app.models.database import get_db
from app.services.key_service import add_identity,delete_identity,update_Identity_key
from app.utils.response import make_response

system_router = APIRouter()

@system_router.get("/health")
def health_route():
    return {
        "Health":"System is working"
    }

@system_router.post("/identity")
def add_identity_route(identity:identityModel,db=Depends(get_db)):
    response = add_identity(db,identity.model_dump())
    return make_response(response)

@system_router.delete("/identity")
def add_identity_route(identity:identityModel,db=Depends(get_db)):
    response = delete_identity(db,identity.model_dump())
    return make_response(response)

@system_router.patch("/token")
def add_identity_route(identity:identityModel,db=Depends(get_db)):
    response = update_Identity_key(db,identity.model_dump())
    return make_response(response)