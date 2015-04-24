#!/usr/bin/python3

from functools import wraps

from bottle import get, post, request, run, static_file, redirect, abort, error, hook as bottle_hook

from models import Entry, User

from urls import URLS
import views
from lib.Session import Session

from settings import DEBUG, STATIC_DIR


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = Session.get_user()
        if user is None:
            return redirect(URLS['signin'])
        return f(*args, **kwargs)
    return decorated


@bottle_hook('before_request')
def insert_slash():
    request_url = request.environ['PATH_INFO']  # type: str

    if request_url.startswith('/static/'):
        return None
    if request_url.find('?') > 0:
        return None
    if request_url.endswith('/'):
        return None
    if request_url.endswith('index.py'):
        return None
    redirect(request_url + '/')


@get('/index.py')
@get(URLS['index'])
def index_view():
    template_name = 'index.html'

    entries = Entry.select().where(Entry.parent == None, Entry.is_active == True)

    return views.render(template_name, entries=entries, is_index=True)


@get(URLS['entry'])
def entry_view(entry_id):
    template_name = 'index.html'

    if Entry.select().where(Entry.id == entry_id, Entry.is_active == True, Entry.parent == None).exists():
        entries = Entry.select().where(Entry.id == entry_id, Entry.is_active == True)
        responses = Entry.select().where(Entry.parent << entries)
    else:
        abort(404)

    return views.render(template_name, entries=entries, responses=responses, is_entry=True)


@post(URLS['signup'])
def signup_view():
    username = views.form_get('username', None)
    password = views.form_get('password', None)

    if username is None or password is None:
        abort(404)

    if User.select().where(User.username == username).exists():
        abort(404)

    user = User.create(
        username=username,
        password=password,
    )

    Session.signin(user)

    return redirect(URLS['index'])


@post(URLS['signin'])
def signin_view():
    user = Session.get_user()
    if user is not None:
        Session.signout()

    username = views.form_get('username', None)
    password = views.form_get('password', None)

    if User.select().where(User.username == username, User.password == password, User.is_active == True).exists():
        user = User.get(User.username == username, User.password == password, User.is_active == True)
    else:
        abort(404)

    Session.signin(user)

    return redirect(URLS['index'])


@get(URLS['signout'])
@requires_login
def signout_view():
    Session.signout()

    return redirect(URLS['index'])


@post(URLS['new'])
@post(URLS['new.response'])
@requires_login
def new_view(parent_id=None):
    user = Session.get_user()

    if parent_id and Entry.select().where(Entry.id == parent_id, Entry.is_active == True).exists():
        parent = Entry.get(Entry.id == parent_id, Entry.is_active == True)
    else:
        parent = None

    title = views.form_get('title', 'no title')
    body = views.form_get('body', '')

    Entry.create(
        user=user,
        parent=parent,
        title=title,
        body=body,
    )

    return redirect(URLS['index'])


@post(URLS['remove'])
@requires_login
def remove_view(entry_id):
    user = Session.get_user()

    if Entry.select().where(Entry.id == entry_id, Entry.user == user, Entry.is_active == True).exists():
        entry = Entry.get(Entry.user == user, Entry.is_active == True)
        entry.is_active = False
        entry.save()
    else:
        abort(404)

    return redirect(URLS['index'])


@post(URLS['user.setting'])
@requires_login
def user_setting_view():
    user = Session.get_user()

    user.setting.nickname = views.form_get('nickname', 'Anonymous')
    user.setting.body = views.form_get('body', '')
    user.setting.save()

    return redirect(URLS['index'])


@get("/static/<filename:path>")
def static_view(filename):
    return static_file(filename, root=STATIC_DIR)


@error(404)
def error404(error):
    return views.render("404.html")


@error(500)
def error500(error):
    return views.render("500.html")


@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_DIR)


if __name__ == '__main__':
    if DEBUG is True:
        run(host='localhost', port=8080, reloader=True, debug=True)
    else:
        run(server='cgi')
