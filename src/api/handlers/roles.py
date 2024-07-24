from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.services.users.users import get_user_by_id, update_user
from src.api.schemas.users import UpdatedUserResponse
from src.database.session import connect_to_db
from src.api.services.auth.auth import get_current_user_from_token
from src.database.models.models import User

role_router = APIRouter()

@role_router.patch("/add_privileges", response_model=UpdatedUserResponse)
async def give_admin_privileges(
    user_id: UUID, 
    db: AsyncSession = Depends(connect_to_db),
    current_user: User = Depends(get_current_user_from_token)
) -> UpdatedUserResponse: 
    if current_user.user_id == user_id: 
        raise HTTPException(status_code=400, detail=f"Cannot manage privilege to itself")
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden")
    user_for_promotiom = await get_user_by_id(user_id, db)
    if user_for_promotiom.is_admin or user_for_promotiom.is_superadmin:
        raise HTTPException(status_code=409, detail=f"User with {user_for_promotiom.username} already has rights")
    if user_for_promotiom is None:
        raise HTTPException(status_code=404, detail=f"User not found")
    updated_user_params = {
        "roles":  user_for_promotiom.add_admin_privilages()
    }
    try: 
        updated_user_id = await update_user(
            user_id=user_id, updated_user_params=updated_user_params, session=db
        )
    except:
        raise HTTPException(status_code=503, detail=f"Database error")
    finally:
        return UpdatedUserResponse(updated_user_id)