from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.databases.postgresql import get_db
from favorite_product_api.exceptions import NotFoundError
from favorite_product_api.users.payloads import CreateUserPayload, UpdateUserPayload
from favorite_product_api.users.responses import CreateUserResponse, UpdateUserResponse
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
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch(
    "/{uuid}", response_model=UpdateUserResponse, response_model_exclude_none=True
)
async def update_user(
    uuid: UUID, payload: UpdateUserPayload, db_session: AsyncSession = Depends(get_db)
):
    try:
        updated_data = await UserService.update_user(
            db_session=db_session, uuid=uuid, name=payload.name, email=payload.email
        )

        return UpdateUserResponse(
            uuid=uuid,
            email=updated_data.get("email", None),
            name=updated_data.get("name", None),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
