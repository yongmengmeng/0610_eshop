from django.shortcuts import redirect
import hashlib


def set_password(password):
    """md5加密"""
    md5 = hashlib.md5()
    md5.update(password.encode())
    new_password = md5.hexdigest()
    return new_password


def wrapper_login(func):
    def inner(request, *args, **kwargs):
        logined = request.session.get('logined')
        if logined:
            return func(request, *args, **kwargs)
        else:
            return redirect('/store/login/')
    return inner
