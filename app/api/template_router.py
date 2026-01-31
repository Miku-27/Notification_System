from fastapi import APIRouter,Depends
from app.models.pydantic_models import TemplateModel
from app.models.database import get_db
from app.services.template_services import add_new_template,remove_template,update_template,get_all_template,get_template_by_slug
from app.dependencies import validate_api_key


template_router = APIRouter()

@template_router.post('')
def add_template_route(template:TemplateModel,db=Depends(get_db),project_id=Depends(validate_api_key)):
    response = add_new_template(db,template.model_dump(),project_id)
    
    return {
        "response":response,
        "template":template
    }

@template_router.delete('/{slug}')
def remove_template_route(slug:str,db=Depends(get_db),project_id=Depends(validate_api_key)):
    response = remove_template(db,slug,project_id)
    
    return {
        "response":response,
        "template":slug
    }

@template_router.put('/{slug}')
def update_template_route(template:TemplateModel,slug:str,db=Depends(get_db),project_id=Depends(validate_api_key)):
    response = update_template(db,TemplateModel,slug,project_id)
    
    return {
        "response":response,
        "template":slug
    }

@template_router.get("")
def get_all_template_route(db=Depends(get_db),project_id=Depends(validate_api_key)):
    response = get_all_template(db,project_id)
   
    return {
        "response":response
    }

@template_router.get("/{slug}")
def get_template_by_slug_route(slug:str,db=Depends(get_db),project_id=Depends(validate_api_key)):
    response = get_template_by_slug(db,slug,project_id)
   
    return {
        "response":response
    }