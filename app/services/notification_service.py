from app.models.model import NotificationTable
from app.services.template_services import _get_template,_resolve_template,_validate_template
from app.utils.response import ResultCodes
from app.utils.exceptions import ServiceException


def register_notification(notification_dict,db):
    try:
        resolved_template = _resolve_template(db,notification_dict)
        custom_template = resolved_template.content if resolved_template.is_custom else None
        _validate_template(resolved_template.content,notification_dict.get("payload"))

        notifications=[]
        recipients = notification_dict['recipient_address']

        for r in recipients:
            notifications.append(NotificationTable(
                sender_address = notification_dict['sender_address'],
                notification_type = notification_dict['mode'],
                recipient_address = r,
                template_id = resolved_template.template_id,
                custom_template=custom_template,
                payload = notification_dict['payload_data'],
                scheduled_at = notification_dict['scheduled_at'],
                priority = notification_dict['priority']
            ))

        
    
        return {
            'success':True,
            'code':ResultCodes.NOTIFICATION_REGISTERED,
        }
    except:
        db.rollback()
        raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)

def _register_single(db,notification_dict):
    if  notification_dict.template:
            template = _get_template(db,notification_dict.get('slug'))
            if template is None:
                return {
                    'success':False,
                    'code':ResultCodes.TEMPLATE_NOT_FOUND,
                }
            
            template_content = template.content
    else:
        template_content = notification_dict.get('content')

    jinja_template_engine = get_template_engine()
    
    response = jinja_template_engine.validate(template_content,notification_dict.get('payload_data'))
    if not response['success']:
        return{
            'success':False,
            'code':response['code']
        }
    
def _register_fanout(db,notification_dict):
    pass

def _check_notificatio