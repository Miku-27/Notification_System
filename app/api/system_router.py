from fastapi import APIRouter,Depends
from app.models.pydantic_models import indentityModel
from app.models.database import get_db
from app.services.key_service import add_indentity
from app.utils.response import make_response
system_router = APIRouter()

@system_router.get("/health")
def health_route():
    return {
        "Health":"System is working"
    }

@system_router.post("/indentity")
def add_indentity_route(indentity:indentityModel,db=Depends(get_db)):
    response = add_indentity(db,indentity.model_dump())
    return make_response(response)
