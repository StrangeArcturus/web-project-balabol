import sqlalchemy
from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, 
        primary_key=True,
        autoincrement=True
    )

    text = sqlalchemy.Column(
        sqlalchemy.String
    )

    def __str__(self) -> str:
        return str(self.text)
