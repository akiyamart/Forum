from fastapi import Depends, HTTPException, status
from uuid import UUID
from logging import getLogger
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.handlers.users.users import user_router, _create_new_user, _get_user_by_id, _get_user_by_email, _delete_user, _update_user
from src.api.models import ShowUser, UserCreate, DeletedUserResponse, UpdatedUserResponse, UpdatedUserRequest
from src.database.session import connect_to_db
from src.database.models import User

logger = getLogger(__name__)

### User
@user_router.post("/", response_model=ShowUser)
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(connect_to_db)
) -> ShowUser: 
    return await _create_new_user(body, db)

@user_router.delete("/", response_model=DeletedUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(connect_to_db) 
    # current_user: User # Потом сюда прикрутить JWT
) -> DeletedUserResponse:
    # user_to_delete = await _get_user_by_id(user_id)
    # if user_to_delete is None: 
    #     raise HTTPException(status_code=404, detail=f"User with {user_id} not found")
    # ADD: Permissions
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None: 
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return DeletedUserResponse(deleted_user_id=deleted_user_id)

@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(connect_to_db)
) -> ShowUser: 
    user_info = await _get_user_by_id(user_id, db)
    if user_info is None: 
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user_info

@user_router.get("/", response_model=ShowUser)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(connect_to_db)
) -> ShowUser: 
    user_info = await _get_user_by_email(email, db)
    if user_info is None: 
        raise HTTPException(status_code=404, detail=f"User with {email} not found")
    return user_info

@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user(
    user_id: UUID, 
    body: UpdatedUserRequest, 
    db: AsyncSession = Depends(connect_to_db),
    # current_user: User = Depends(get_current_user_from_token)
) -> UpdatedUserResponse: 
    updated_user_params = body.model_dump(exclude=True)
    if updated_user_params == {}: 
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    # if not check_user_permissions(target_user=user_for_update, current_user=current_user):
    #     raise HTTPException(status_code=403, detail="Forbidden")
    try:
        updated_user_id = await _update_user(user_id=user_id, session=db, updated_user_params=updated_user_params)
        return UpdatedUserResponse(updated_user_id=updated_user_id)
    except IntegrityError as err: 
        logger.error(err)