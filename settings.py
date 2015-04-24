#!/usr/bin/python3

import socket
import os
import peewee


SITE_URL_BASE = 'http://example.jp/'  # type: str

PAGE_PER_ENTRY = 5  # type: int
PASSWORD = "password"  # type: str

SESSION_LIFE_TIME = 4*24*60*60  # type: int


LOCAL_HOSTNAME = ('x40', '1280jp')  # type: tuple

if socket.gethostname() in LOCAL_HOSTNAME:
    DEBUG = True  # type: bool
    SITE_URL = 'http://localhost:8080/'  # type: str
    STATIC_URL = '/static/'  # type: str
else:
    DEBUG = False  # type: bool
    SITE_URL = SITE_URL_BASE  # type: str
    STATIC_URL = SITE_URL_BASE + 'static/'  # type: str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # type: str
STATIC_DIR = os.path.join(BASE_DIR, 'static')  # type: str
DB_DIR = os.path.join(BASE_DIR, 'db')  # type: str
TEMPLATE_DIR = os.path.join(BASE_DIR, 'template')  # type: str

SITE_DB_FILE_PATH = os.path.join(DB_DIR, 'system.db')  # type: str
SITE_DB = peewee.SqliteDatabase(SITE_DB_FILE_PATH, threadlocals=True)  # type: str
TMP_DB_FILE_PATH = os.path.join(DB_DIR, 'tmp.db')  # type: str
TMP_DB = peewee.SqliteDatabase(TMP_DB_FILE_PATH, threadlocals=True)  # type: str