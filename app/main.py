from fastapi import FastAPI,exception_handlers
from app.api.notification_router import notification_router
from app.api.system_router import system_router
from app.api.template_router import template_router
from app.utils.exceptions import ServiceException
from app.utils.response import make_response

app = FastAPI()


@app.exception_handler(ServiceException)
async def handle_service_exception(exc:ServiceException):
    make_response({
        "success":False,
        "code":exc.code,
        "data":exc.data
    })


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