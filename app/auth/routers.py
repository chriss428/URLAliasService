from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from app.schemas import UserCreate
from app.auth.crud import create_user, get_auth_user_or_none
from app.auth.auth import get_password_hash, get_current_user


router = APIRouter(prefix="/auth", tags=["Регистрация/Аутентификация"])


@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: UserCreate):
    user = await get_auth_user_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    await create_user(user_dict)
    return {"status": "success"}


@router.get("/users/me", summary="Аутетификация")
async def read_current_user(email: Annotated[str, Depends(get_current_user)]):
    user = await get_auth_user_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user.email, "id": user.id}
