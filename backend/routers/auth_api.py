from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..sqlm.sqlm_tables import User
from ..pydm.schemas import UserCreate,TokenOut
from .dependencies import async_get_db

from ..setup.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(data: UserCreate, db: AsyncSession = Depends(async_get_db)):
    existing = await db.execute(
        select(User).where(User.email == data.email)
    )
    if existing.scalar():
        raise HTTPException(400, detail="Email already registered")

    new_user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(new_user)
    await db.commit()
    return {"msg": "User created"}

@router.post("/login", response_model=TokenOut)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(async_get_db)
):
    print("STARTED HERE LOGIN ------------------")
    result = await db.execute(select(User).where(User.email == username))
    
    print("dont even reach here....")
    user = result.scalar_one_or_none()

    print("user", user)
    if not user or not verify_password(password, user.password):
        raise HTTPException(401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}

