from app.models.model import TemplateTable

def _get_template_id(db,slug_name):
    template_id = db.query(TemplateTable.id).filter(TemplateTable.slug == slug_name).first()
    if template_id:
        return template_id
    return None
    