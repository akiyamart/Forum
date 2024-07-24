from fastapi import Depends, APIRouter, HTTPException, Query
from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.services.users.users import create_new_user, get_user_by_id, find_user, delete_user, update_user, check_user_permissions
from src.api.schemas.users import ShowUserResponse, UserCreate, DeletedUserResponse, UpdatedUserResponse, UpdatedUserRequest
from src.database.session import connect_to_db
from src.api.services.auth.auth import get_current_user_from_token
from src.database.models.models import User

user_router = APIRouter()

@user_router.post("/", response_model=ShowUserResponse)
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(connect_to_db)
) -> ShowUserResponse: 
    new_user = await create_new_user(body, db)
    if new_user is None: 
        raise HTTPException(status_code=409, detail="Username or email already taken")
    return new_user

@user_router.delete("/", response_model=DeletedUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(connect_to_db),
    current_user: User = Depends(get_current_user_from_token)
) -> DeletedUserResponse:
    user_to_delete = await get_user_by_id(user_id)
    if user_to_delete is None: 
        raise HTTPException(status_code=404, detail=f"User with {user_id} not found")
    if not check_user_permissions( 
        target_user=user_to_delete, 
        current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    deleted_user_id = await delete_user(user_id, db)
    if deleted_user_id is None: 
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return DeletedUserResponse(deleted_user_id=deleted_user_id)

@user_router.get("/", response_model=ShowUserResponse)
async def get_user(
    uuid: Optional[UUID] = Query(None),
    email: Optional[str] = Query(None),
    db: AsyncSession = Depends(connect_to_db)
) -> ShowUserResponse: 
    user_info = await find_user(uuid, email, db)
    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info

@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user(
    user_id: UUID, 
    body: UpdatedUserRequest, 
    db: AsyncSession = Depends(connect_to_db),
    current_user: User = Depends(get_current_user_from_token)
) -> UpdatedUserResponse: 
    updated_user_params = body.model_dump(exclude_none=True)
    if updated_user_params == {}: 
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user_for_update = await get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    if not check_user_permissions(target_user=user_for_update, current_user=current_user):
        raise HTTPException(status_code=403, detail="Forbidden")
    updated_user_id = await update_user(user_id=user_id, session=db, updated_user_params=updated_user_params)
    if updated_user_id is None: 
        raise HTTPException(status_code=409, detail="Username or email already taken")
    return UpdatedUserResponse(updated_user_id=updated_user_id)

