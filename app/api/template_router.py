from fastapi import APIRouter,Depends
from app.models.pydantic_models import TemplateModel
from app.models.database import get_db
from app.services.template_services import add_new_template,remove_template,update_template,get_all_template,get_template_by_slug
from app.dependencies import validate_api_key
from app.utils.response import make_response


template_router = APIRouter()

@template_router.post('')
def add_template_route(template:TemplateModel,db=Depends(get_db),identity_id=Depends(validate_api_key)):
    response = add_new_template(db,template.model_dump(),identity_id)
    
    return make_response(response)

@template_router.delete('/{slug}')
def remove_template_route(slug:str,db=Depends(get_db),identity_id=Depends(validate_api_key)):
    response = remove_template(db,slug,identity_id)
    
    return make_response(response)

@template_router.put('/{slug}')
def update_template_route(template:TemplateModel,slug:str,db=Depends(get_db),identity_id=Depends(validate_api_key)):
    response = update_template(db,TemplateModel,slug,identity_id)
    
    return make_response(response)

@template_router.get("")
def get_all_template_route(db=Depends(get_db),identity_id=Depends(validate_api_key)):
    response = get_all_template(db,identity_id)
   
    return make_response(response)

@template_router.get("/{slug}")
def get_template_by_slug_route(slug:str,db=Depends(get_db),identity_id=Depends(validate_api_key)):
    response = get_template_by_slug(db,slug,identity_id)
   
    return make_response(response)