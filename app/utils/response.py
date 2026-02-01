from enum import Enum
from fastapi import status
from fastapi.responses import JSONResponse

class ResultCodes(str,Enum):
    TEMPLATE_ADDED = "TEMPLATE_ADDED"
    TEMPLATE_ALREADY_EXIST = "TEMPLATE_ALREADY_EXIST"
    TEMPLATE_NOT_FOUND = "TEMPLATE_NOT_FOUND"
    TEMPLATE_DELETED = "TEMPLATE_DELETED"
    TEMPLATE_UPDATED = "TEMPLATE_UPDATED"

    IDENTITY_CREATED = "IDENTITY_CREATED"
    IDENTITY_DELETED = "IDENTITY_DELETED"
    IDENTITY_UPDATED = "IDENTITY_UPDATED"
    IDENTITY_NOT_FOUND = "IDENTITY_NOT_FOUND"
    IDENTITY_ALREADY_EXIST = "IDENTITY_ALREADY_EXIST"
    IDENTITY_VERIFIED = "IDENTITY_VERIFIED"
    IDENTITY_INVALID = "IDENTITY_INVALID"

    NOTIFICATION_REGISTERED = "NOTIFICATION_REGISTERED"

    DATA_RETRIVED = "DATA_RETRIVED"
    OPERATION_COMPLETED = "OPERATION_COMPLETED" 
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR" 

from fastapi import status

HTTP_CODE_MAP = {

    "TEMPLATE_ADDED": status.HTTP_201_CREATED,
    "TEMPLATE_ALREADY_EXIST": status.HTTP_409_CONFLICT,
    "TEMPLATE_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "TEMPLATE_DELETED": status.HTTP_200_OK,
    "TEMPLATE_UPDATED": status.HTTP_200_OK,

    "IDENTITY_CREATED": status.HTTP_201_CREATED,
    "IDENTITY_DELETED": status.HTTP_200_OK,
    "IDENTITY_UPDATED": status.HTTP_200_OK,
    "IDENTITY_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "IDENTITY_ALREADY_EXIST": status.HTTP_409_CONFLICT,
    "IDENTITY_VERIFIED": status.HTTP_200_OK,
    "IDENTITY_INVALID": status.HTTP_401_UNAUTHORIZED,

    "NOTIFICATION_REGISTERED": status.HTTP_202_ACCEPTED,

    "DATA_RETRIVED": status.HTTP_200_OK,
    "OPERATION_COMPLETED": status.HTTP_200_OK,
    "INTERNAL_SERVER_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR
}

MESSAGE_MAP = {
    "TEMPLATE_ADDED": "Template has been successfully added.",
    "TEMPLATE_ALREADY_EXIST": "A template with this name already exists.",
    "TEMPLATE_NOT_FOUND": "The requested template could not be found.",
    "TEMPLATE_DELETED": "Template has been successfully deleted.",
    "TEMPLATE_UPDATED": "Template has been successfully updated.",

    "IDENTITY_CREATED": "Identity and API key created successfully.",
    "IDENTITY_DELETED": "Identity has been removed from the system.",
    "IDENTITY_UPDATED": "Identity details have been updated.",
    "IDENTITY_NOT_FOUND": "No identity found with the provided details.",
    "IDENTITY_ALREADY_EXIST": "This identity name is already in use.",
    "IDENTITY_VERIFIED": "Identity successfully verified.",
    "IDENTITY_INVALID": "Invalid identity name or API key.",

    "NOTIFICATION_REGISTERED": "Notification has been queued for delivery.",

    "DATA_RETRIVED": "Data retrieved successfully.",
    "OPERATION_COMPLETED": "The requested operation was completed.",
    "INTERNAL_SERVER_ERROR": "An unexpected error occurred on the server."
}

def make_response(service_response):
    success = service_response.get('success')
    code = service_response.get('code')
    data = service_response.get('data',None)

    http_code = HTTP_CODE_MAP.get(code)
    msg = MESSAGE_MAP.get(code)

    response_obj = JSONResponse(
        status_code=http_code,
        content={
            "success": success,
            "msg": msg,
            "data": data,
        }
    )
    
    return response_obj


    