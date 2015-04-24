#!/usr/bin/python3

import bottle
from bottle import request
from bottle import jinja2_template as template

from settings import TEMPLATE_DIR, PAGE_PER_ENTRY
bottle.TEMPLATE_PATH.insert(0, TEMPLATE_DIR)

from lib.Session import Session


def request_is_get():
    if request.method == 'GET':
        return True
    return False


def request_is_post():
    if request.method == 'POST':
        return True
    return False


def form_get(name, default=None):
    try:
        return request.forms.decode().get(name, default)
    except:
        return request.forms.get(name, default)


def form_getall(name):
    try:
        return request.forms.decode().getall(name)
    except:
        return request.forms.getall(name)


def parse_parameter():
    default_page = 1

    return {
        'page': int(request.query.page or default_page)
    }


def make_parameter(parameter):
    url = '?'

    for key, value in parameter.items():
        if value is True or str(value).isdigit():
            url += '{0}={1}&'.format(key, value)

    return url


def render(template_name, **kwargs):
    user = Session.get_user()
    parameter = parse_parameter()
    return template(template_name, user=user, parameter=parameter, PAGE_PER_ENTRY=PAGE_PER_ENTRY, **kwargs)
