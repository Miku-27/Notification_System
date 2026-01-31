from fastapi import FastAPI
from app.api.notification_router import notification_router
from app.api.system_router import system_router
from app.api.template_router import template_router
app = FastAPI()

app.include_router(
    router=notification_router,
    prefix="/notification",
    tags=["notification"]
)

app.include_router(
    router=system_router,
    prefix="/system",
    tags=["system"]
)

app.include_router(
    router=template_router,
    prefix="/template",
    tags=["template"]
)