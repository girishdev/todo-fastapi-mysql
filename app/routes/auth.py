from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import (
    UserRepository,
)
from app.schemas import (
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.services import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_auth_service(
    db: Session = Depends(
        get_db
    ),
) -> AuthService:

    repository = UserRepository(
        db
    )

    return AuthService(
        repository
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=(
        status.HTTP_201_CREATED
    ),
)
def register(
    user_data: UserCreate,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    return service.register(
        user_data
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data:
        OAuth2PasswordRequestForm
        = Depends(),

    service: AuthService = Depends(
        get_auth_service
    ),
):

    return service.login(
        email=form_data.username,
        password=form_data.password,
    )