from fastapi import APIRouter,Depends
from app.models.pydantic_models import ProjectModel
from app.models.database import get_db
from app.services.key_service import add_project

system_router = APIRouter()

@system_router.get("/health")
def health_route():
    return {
        "Health":"System is working"
    }

@system_router.post("/project")
def add_project_route(project:ProjectModel,db=Depends(get_db)):
    response = add_project(db,project.model_dump())
    return response
