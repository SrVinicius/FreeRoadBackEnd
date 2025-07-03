from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from blog.api.deps import user_repo
from blog.usecases.user.register_user import RegisterUserUseCase
from blog.usecases.user.login_user import LoginUserUseCase
from blog.usecases.user.logout_user import LogoutUserUseCase
from blog.usecases.user.get_current_user import GetCurrentUserUseCase
from blog.usecases.user.set_current_user import SetCurrentUserUseCase
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
import uuid

from blog.api.schemas.user_schema import (
    RegisterUserInput,
    LoginUserInput,
    UserOutput,
    RegisterUserResponse,
)

router = APIRouter()

# ----------------------
# Register
# ----------------------


@router.post(
    "/register",
    response_model=RegisterUserResponse,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com nome, email e senha forte.",
)
def register_user(data: RegisterUserInput):
    try:
        user = User(
            id=str(uuid.uuid4()),
            name=data.name,
            email=Email(data.email),
            password=Password(data.password),
            role=data.role,
        )
        usecase = RegisterUserUseCase(user_repo)
        result = usecase.execute(user)
        return RegisterUserResponse(
            message="User registered successfully",
            result=UserOutput(
                id=result.id,
                name=result.name,
                email=str(result.email.value),
                role=result.role,
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------
# Login
# ----------------------


@router.post(
    "/login",
    response_model=UserOutput,
    summary="Fazer o Login do usuário",
    description="Autentica um usuário com email e senha forte.",
)
def login_user(data: LoginUserInput):
    try:
        usecase = LoginUserUseCase(user_repo)
        result = usecase.execute(Email(data.email), Password(data.password))
        return {"message": "Login successful", "user": result}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# ----------------------
# Logout
# ----------------------


@router.post(
    "/logout",
    summary="Fazer o Logout do usuário",
    description="Descredencia o usuário autenticado.",
)
def logout_user():
    usecase = LogoutUserUseCase(user_repo)
    usecase.execute()
    return {"message": "Logout successful"}


# ----------------------
# Get Current User
# ----------------------


@router.get(
    "/me",
    response_model=UserOutput,
    summary="Informar os dados do usuário atual",
    description="Retorna os dados do usuário atual.",
)
def get_current_user():
    try:
        usecase = GetCurrentUserUseCase(user_repo)
        result = usecase.execute()
        return {
            "id": result.id,
            "name": result.name,
            "email": str(result.email),
            "role": result.role,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
