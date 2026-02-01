from app.models.model import TemplateTable
from app.utils.response import ResultCodes

def _get_template_id(db,slug_name):
    template_id = db.query(TemplateTable.id).filter(TemplateTable.slug == slug_name).first()
    if template_id:
        return template_id
    return None
    
def add_new_template(db,template_dict,indentity_id):
    try:       
        template_exist = db.query(TemplateTable).filter(TemplateTable.slug == template_dict['slug']).first()
        if template_exist:
            return {
                'success':False,
                'code':ResultCodes.TEMPLATE_ALREADY_EXIST
            }

        new_template = TemplateTable(**template_dict,owner_id=indentity_id)
        db.add(new_template)
        db.commit()
        return {
            'success':True,
            'code':ResultCodes.TEMPLATE_ADDED
        }
    except Exception as e:
        print(e)
        db.rollback()
        return {
            'success':False,
            'code':ResultCodes.INTERNAL_SERVER_ERROR
        }
    
def remove_template(db,slug,indentity_id):
    try:       
        template_exist = db.query(TemplateTable).filter(
            TemplateTable.slug == slug,
            TemplateTable.owner_id == indentity_id
        ).first()

        if not template_exist:
            return {
                'success':False,
                'code':ResultCodes.TEMPLATE_NOT_FOUND
            }

        db.delete(template_exist)
        db.commit()
        return {
            'success':True,
            'code':ResultCodes.TEMPLATE_DELETED
        }
    except Exception as e:
        print(e)
        db.rollback()
        return {
            'success':False,
            'code':ResultCodes.INTERNAL_SERVER_ERROR
        }
    
def update_template(db,template_dict,slug,indentity_id):
    try:       
        template_exist = db.query(TemplateTable).filter(
            TemplateTable.slug == slug,
            TemplateTable.owner_id == indentity_id
        ).first()

        if not template_exist:
            return {
                'success':False,
                'code':ResultCodes.TEMPLATE_NOT_FOUND
            }

        for key,value in template_dict.items():
            setattr(template_exist,key,value)
        template_exist.owner_id=indentity_id

        db.commit()
        return {
            'success':True,
            'code':ResultCodes.TEMPLATE_UPDATED
        }
    except Exception as e:
        print(e)
        db.rollback()
        return {
            'success':False,
            'code':ResultCodes.INTERNAL_SERVER_ERROR
        }

def get_all_template(db,indentity_id):
    try:       
        template_list = db.query(TemplateTable.slug,TemplateTable.template_name).filter(
            TemplateTable.owner_id == indentity_id
        ).all()

        return {
            'success':True,
            'code':ResultCodes.DATA_RETRIVED,
            'data': [{'slug':row.slug,'template_name':row.template_name} for row in template_list]
        }
    except Exception as e:
        print(e)
        return {
            'success':False,
            'code':ResultCodes.INTERNAL_SERVER_ERROR
        }
    
def get_template_by_slug(db,slug,indentity_id):
    try:       
        template_list = db.query(
            TemplateTable.slug,
            TemplateTable.template_name,
            TemplateTable.subject,
            TemplateTable.title,
            TemplateTable.template_body).filter(

            TemplateTable.owner_id == indentity_id,
            TemplateTable.slug == slug
        ).first()

        return {
            'success':True,
            'code':ResultCodes.DATA_RETRIVED,
            'data': template_list._asdict()
        }
    except Exception as e:
        print(e)
        return {
            'success':False,
            'code':ResultCodes.INTERNAL_SERVER_ERROR
        }