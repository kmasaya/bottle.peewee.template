#!/usr/bin/python3

import os
import sys
import time
import datetime
import hashlib
sys.path.append(os.pardir)

from bottle import response, request

from settings import SESSION_LIFE_TIME

import peewee
from models import User, Session as SessionModel


class Session:
    @staticmethod
    def signin(user):
        site_id = hashlib.sha256(repr(time.time()).encode()).hexdigest()
        response.set_cookie('site_id', site_id, max_age=SESSION_LIFE_TIME, path='/')
        response.set_cookie('username', user.username, max_age=SESSION_LIFE_TIME, path='/')

        session = SessionModel.create(
            site_id=site_id,
            username=user.username,
            signined_at=datetime.datetime.now()
        )

    @staticmethod
    def signout():
        site_id = request.get_cookie('site_id', None)

        response.delete_cookie('site_id')
        response.delete_cookie('username')

        if site_id is not None:
            query = SessionModel.delete().where(SessionModel.site_id == site_id)
            query.execute()

    @staticmethod
    def get_user():
        site_id = request.get_cookie('site_id', None)
        username = request.get_cookie('username', None)

        if site_id is None:
            return None

        try:
            SessionModel.get(
                SessionModel.site_id == site_id,
                SessionModel.username == username,
                SessionModel.signined_at > datetime.datetime.now() - datetime.timedelta(seconds=SESSION_LIFE_TIME),
                )
        except peewee.DoesNotExist:
            return None

        try:
            user = User.get(User.username == username, User.is_active == True)
        except peewee.DoesNotExist:
            Session.signout()
            return None

        return user


