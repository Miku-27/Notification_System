from app.models.model import NotificationTable
from app.services.template_services import _get_template_id


def register_notification(notification_data,db):
    try:
        template_id = _get_template_id(db,notification_data.template)
        notification = NotificationTable(**notification_data.model_dump(exclude={"template"}),template_id=template_id)

        db.add(notification)
        db.commit()
        return True
    except:
        db.rollback()
        return False
    