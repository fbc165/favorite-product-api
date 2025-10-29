from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.databases.postgresql import get_db
from favorite_product_api.users.payloads import CreateUserPayload
from favorite_product_api.users.responses import CreateUserResponse
from favorite_product_api.users.services import UserService

router = APIRouter()


@router.post("/")
async def create_user(
    payload: CreateUserPayload, db_session: AsyncSession = Depends(get_db)
):
    try:
        user = await UserService.create_user(
            db_session=db_session, name=payload.name, email=payload.email
        )
        return CreateUserResponse(uuid=user.uuid, email=user.email, name=user.name)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
