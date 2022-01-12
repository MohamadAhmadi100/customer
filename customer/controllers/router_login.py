from fastapi import APIRouter

router_login = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"error": "Not found"}},
)


@router_login.post("/test/")
async def root():
    # TODO fixed status code
    massage = {
        "massage": "You are already registered",
    }
    return massage
