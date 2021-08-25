from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

import service
from ws_client import notify

router = APIRouter(prefix="/v1/notification")


@router.get("/")
def get_notification(_id: str = "", active: bool = True, users=[]):
    print(_id, active, users)
    return "Notifications"


@router.post("/")
async def save_notification(notification: dict):
    new_notification = service.cretate_notification(notification)
    await notify()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=dict(new_notification)
    )
