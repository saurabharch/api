"""
    cloudplayer.api.model.token
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by the cloudplayer team
    :license: GPL-3.0, see LICENSE for details
"""
import functools

from sqlalchemy.sql import func
import sqlalchemy as sql
import sqlalchemy.orm as orm

from cloudplayer.api.model import Base
from cloudplayer.api.util import gen_token


class Token(Base):

    __tablename__ = 'token'
    __fields__ = [
        'id',
        'claimed',
        'expiration'
    ]
    __filters__ = []
    __mutable__ = [
        'claimed'
    ]
    __public__ = []
    __table_args__ = (
        sql.PrimaryKeyConstraint(
            'id'),
        sql.ForeignKeyConstraint(
            ['account_id', 'provider_id'],
            ['account.id', 'account.provider_id'])
    )

    id = sql.Column(sql.String(16), default=functools.partial(gen_token, 6))

    claimed = sql.Column(sql.Boolean, default=False)

    provider_id = sql.Column(
        sql.String(16), nullable=False, default='cloudplayer')
    account_id = sql.Column(sql.String(32), nullable=False)

    created = sql.Column(
        sql.DateTime(timezone=True), server_default=func.now())
    updated = sql.Column(
        sql.DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now())
