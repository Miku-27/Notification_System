from app.models.model import NotificationTable
from app.services.template_services import _get_template_id


def register_notification(notification_dict,db):
    try:
        template_id = _get_template_id(db,notification_dict.template)
        if not template_id:
            return False
        
        notification_dict.pop("template")
        notification = NotificationTable(**notification_dict,template_id=template_id)

        db.add(notification)
        db.commit()
        return True
    except:
        db.rollback()
        return False
    