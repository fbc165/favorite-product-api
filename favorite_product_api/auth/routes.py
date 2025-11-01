from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.auth.auth import (
    create_access_token,
)
from favorite_product_api.auth.payloads import UserLoginPayload
from favorite_product_api.auth.security import verify_password
from favorite_product_api.databases.postgresql import get_db
from favorite_product_api.users.services import UserService

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    payload: UserLoginPayload, db_session: AsyncSession = Depends(get_db)
):
    user = await UserService.get_user_by_email(
        db_session=db_session, email=payload.email
    )
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
