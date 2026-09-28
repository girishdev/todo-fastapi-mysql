from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.exc import IntegrityError

from app.repositories import UserRepository
from app.schemas import (
    TokenResponse,
    UserCreate,
)
from app.security.jwt import (
    create_access_token,
)
from app.security.password import (
    hash_password,
    verify_password,
)


class AuthService:

    def __init__(
        self,
        user_repository: UserRepository,
    ):

        self.user_repository = (
            user_repository
        )


    def register(
        self,
        user_data: UserCreate,
    ):

        email = (
            str(user_data.email)
            .strip()
            .lower()
        )

        existing_user = (
            self.user_repository
            .get_by_email(email)
        )

        if existing_user:

            raise HTTPException(
                status_code=(
                    status.HTTP_409_CONFLICT
                ),
                detail=(
                    "Email already registered"
                ),
            )

        hashed_password = hash_password(
            user_data.password
        )

        try:

            return (
                self.user_repository
                .create(
                    name=user_data.name,
                    email=email,
                    password_hash=(
                        hashed_password
                    ),
                )
            )

        except IntegrityError:

            raise HTTPException(
                status_code=(
                    status.HTTP_409_CONFLICT
                ),
                detail=(
                    "Email already registered"
                ),
            )


    def login(
        self,
        email: str,
        password: str,
    ) -> TokenResponse:

        email = (
            email
            .strip()
            .lower()
        )

        user = (
            self.user_repository
            .get_by_email(email)
        )

        if (
            user is None
            or not verify_password(
                password,
                user.password_hash,
            )
        ):

            raise HTTPException(
                status_code=(
                    status.HTTP_401_UNAUTHORIZED
                ),
                detail=(
                    "Invalid email or password"
                ),
                headers={
                    "WWW-Authenticate":
                    "Bearer"
                },
            )

        if not user.is_active:

            raise HTTPException(
                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
                detail="User is inactive",
            )

        access_token = (
            create_access_token(
                subject=str(user.id)
            )
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
        )