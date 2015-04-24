#!/usr/bin/python3

import datetime

import peewee
from peewee import BooleanField, CharField, TextField, DateTimeField, ForeignKeyField

from settings import SITE_DB, TMP_DB


class SystemModel(peewee.Model):
    class Meta:
        database = SITE_DB


class Setting(SystemModel):
    nickname = CharField(max_length=32, default='Anonymous')
    body = TextField(default='')


class User(SystemModel):
    username = CharField(max_length=128, unique=True)
    password = CharField(max_length=64)
    setting = ForeignKeyField(Setting, unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True)

    @classmethod
    def create(cls, **query):
        setting = Setting.create()
        instance = cls(setting=setting, **query)
        instance.save(force_insert=True)
        instance._prepare_instance()
        return instance


class Entry(SystemModel):
    user = ForeignKeyField(User)
    parent = ForeignKeyField('self', null=True, default=None)
    title = CharField(max_length=64)
    body = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True)

    class Meta():
        order_by = ("-created_at",)
        datetime = SITE_DB


class TmpModel(peewee.Model):
    class Meta:
        database = TMP_DB


class Session(TmpModel):
    site_id = CharField(max_length=128)
    username = CharField(max_length=128)
    signined_at = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True)


if __name__ == '__main__':
    Setting.create_table()
    User.create_table()
    Entry.create_table()
    Session.create_table()