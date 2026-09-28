from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jwt.exceptions import (
    InvalidTokenError,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.repositories import (
    UserRepository,
)
from app.security.jwt import (
    decode_access_token,
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    ),
    db: Session = Depends(
        get_db
    ),
) -> User:

    credentials_exception = (
        HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Could not validate credentials"
            ),
            headers={
                "WWW-Authenticate":
                "Bearer"
            },
        )
    )

    try:

        payload = decode_access_token(
            token
        )

        subject = payload.get(
            "sub"
        )

        if subject is None:

            raise credentials_exception

        user_id = int(subject)

    except (
        InvalidTokenError,
        ValueError,
        TypeError,
    ):

        raise credentials_exception

    repository = UserRepository(
        db
    )

    user = repository.get_by_id(
        user_id
    )

    if user is None:

        raise credentials_exception

    if not user.is_active:

        raise HTTPException(
            status_code=(
                status.HTTP_403_FORBIDDEN
            ),
            detail="User is inactive",
        )

    return user