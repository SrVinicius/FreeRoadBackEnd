from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from freeroad.api.deps import user_repo
from freeroad.usecases.user.register_user import RegisterUserUseCase
from freeroad.usecases.user.login_user import LoginUserUseCase
from freeroad.usecases.user.logout_user import LogoutUserUseCase
from freeroad.usecases.user.get_current_user import GetCurrentUserUseCase
from freeroad.usecases.user.set_current_user import SetCurrentUserUseCase
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password
import uuid
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from freeroad.api.schemas.user_schema import (
    RegisterUserInput,
    LoginUserInput,
    UserOutput,
    RegisterUserResponse,
)

router = APIRouter()

security = HTTPBearer()

async def get_current_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = await user_repo.get_current_user()
    if not user or user.id != token:
        raise HTTPException(status_code=401, detail="Usuário não autenticado.")
    return user

# ----------------------
# Login
# ----------------------

@router.post("/login")
async def login_user(data: LoginUserInput):
    user = await user_repo.get_by_email(Email(data.email))
    if not user or not user.password.verify(data.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    await user_repo.set_current_user(user)
    return {"access_token": user.id, "token_type": "bearer"}

# ----------------------
# Logout
# ----------------------

@router.post(
    "/logout",
    summary="Fazer o Logout do usuário",
    description="Descredencia o usuário autenticado.",
)
async def logout_user(user=Depends(get_current_user_token)):
    try:
        usecase = LogoutUserUseCase(user_repo)
        await usecase.execute()
        return {"message": "Logout successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------------
# Get Current User
# ----------------------

@router.get(
    "/me",
    response_model=UserOutput,
    summary="Informar os dados do usuário atual",
    description="Retorna os dados do usuário atual.",
)
async def get_current_user_route(user=Depends(get_current_user_token)):
    return {
        "id": user.id,
        "name": user.name,
        "email": str(user.email.value),
        "role": user.role,
    }

# ----------------------
# Register
# ----------------------

@router.post(
    "/register",
    response_model=RegisterUserResponse,
    status_code=201,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com nome, email e senha forte.",
)
async def register_user(
    data: RegisterUserInput,
):
    try:
        # Check for duplicate email
        existing_user = await user_repo.get_by_email(Email(data.email))
        if existing_user:
            raise HTTPException(status_code=400, detail="Email já está registrado.")

        user_obj = User(
            id=str(uuid.uuid4()),
            name=data.name,
            email=Email(data.email),
            password=Password(data.password),  # Validate password during registration
            role=data.role,
        )
        usecase = RegisterUserUseCase(user_repo)
        result = await usecase.execute(user_obj)
        return RegisterUserResponse(
            message="User registered successfully",
            user=UserOutput(
                id=result.id,
                name=result.name,
                email=str(result.email.value),
                role=result.role,
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
