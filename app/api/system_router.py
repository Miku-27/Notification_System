from fastapi import APIRouter

system_router = APIRouter()

@system_router.get("/health")
def health_route():
    return {
        "Health":"System is working"
    }