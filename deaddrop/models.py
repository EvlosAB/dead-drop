import uuid
from .db import db


def get_uuid():
    return str(uuid.uuid4())


class EncryptedInformation(db.Model):
    __tablename__ = 'encrypted_information'

    id = db.Column(
        db.Integer(),
        primary_key=True,
        unique=True,
        nullable=False,
    )

    uuid = db.Column(
        db.String(255),
        nullable=False,
        default=get_uuid,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )

    token = db.Column(
        db.Binary(),
        nullable=False,
    )
