from app.models.model import NotificationTable
from app.services.template_services import _get_template_id
from app.utils.response import ResultCodes

def register_notification(notification_dict,db):
    try:
        template_id = _get_template_id(db,notification_dict.template)
        if not template_id:
            return {
                'success':False,
                'code':ResultCodes.TEMPLATE_NOT_FOUND,
            }
        
        notification_dict.pop("template")
        notification = NotificationTable(**notification_dict,template_id=template_id)

        db.add(notification)
        db.commit()
        return {
            'success':True,
            'code':ResultCodes.NOTIFICATION_REGISTERED,
        }
    except:
        db.rollback()
        return {
            'success':True,
            'code':ResultCodes.INTERNAL_SERVER_ERROR,
        }
    