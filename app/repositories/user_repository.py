from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        query = (
            select(User)
            .where(
                User.email == email
            )
        )

        return self.db.scalar(
            query
        )


    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return self.db.get(
            User,
            user_id,
        )


    def create(
        self,
        name: str,
        email: str,
        password_hash: str,
    ) -> User:

        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
        )

        try:

            self.db.add(user)

            self.db.commit()

            self.db.refresh(user)

            return user

        except SQLAlchemyError:

            self.db.rollback()

            raise