from app.models.model import TemplateTable

def _get_template_id(db,slug_name):
    template_id = db.query(TemplateTable.id).filter(TemplateTable.slug == slug_name).first()
    if template_id:
        return template_id
    return None
    
def add_new_template(db,template_dict,project_id):
    try:       
        template_exist = db.query(TemplateTable).filter(TemplateTable.slug == template_dict['slug']).first()
        if template_exist:
            return False

        new_template = TemplateTable(**template_dict,owner_id=project_id)
        db.add(new_template)
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
    
def remove_template(db,slug,project_id):
    try:       
        template_exist = db.query(TemplateTable).filter(
            TemplateTable.slug == slug,
            TemplateTable.owner_id == project_id
        ).first()

        if not template_exist:
            return False

        db.delete(template_exist)
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
    
def update_template(db,template_dict,slug,project_id):
    try:       
        template_exist = db.query(TemplateTable).filter(
            TemplateTable.slug == slug,
            TemplateTable.owner_id == project_id
        ).first()

        if not template_exist:
            return False

        for key,value in template_dict.items():
            setattr(template_exist,key,value)
        template_exist.owner_id=project_id

        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False

def get_all_template(db,project_id):
    try:       
        template_list = db.query(TemplateTable.slug,TemplateTable.template_name).filter(
            TemplateTable.owner_id == project_id
        ).all()

        return [{'slug':row.slug,'template_name':row.template_name} for row in template_list]
    except Exception as e:
        print(e)
        return False
    
def get_template_by_slug(db,slug,project_id):
    try:       
        template_list = db.query(
            TemplateTable.slug,
            TemplateTable.template_name,
            TemplateTable.subject,
            TemplateTable.title,
            TemplateTable.template_body).filter(

            TemplateTable.owner_id == project_id,
            TemplateTable.slug == slug
        ).first()

        return template_list._asdict()
    except Exception as e:
        print(e)
        return False