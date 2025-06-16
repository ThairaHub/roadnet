from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..sqlm.sqlm_tables import User
from ..pydm.schemas import UserOut
from .dependencies import async_get_db
from typing import List


from ..setup.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
async def get_current_user_info(
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=List[UserOut])
async def get_users(
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: int,
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    # Optional: you can restrict access to self/admin here if needed
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete other users")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"msg": "User deleted"}
