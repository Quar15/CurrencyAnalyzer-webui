from flask import session, make_response
from functools import wraps


FLASH_MESSAGE_AVAILABLE_SESSION_VAR = 'flash_message_available'
REFRESH_PAGE_SESSION_VAR = 'refresh_page'


def add_notification_refresh_header(viewmethod):
    @wraps(viewmethod)
    def new_viewmethod(*args, **kwargs):
        resp = make_response(viewmethod(*args, **kwargs))
        if FLASH_MESSAGE_AVAILABLE_SESSION_VAR in session and session[FLASH_MESSAGE_AVAILABLE_SESSION_VAR]:
            resp.headers["HX-Trigger"] = "newNotification"
            session[FLASH_MESSAGE_AVAILABLE_SESSION_VAR] = False
        return resp
    return new_viewmethod


def add_page_refresh_header(viewmethod):
    @wraps(viewmethod)
    def new_viewmethod(*args, **kwargs):
        resp = make_response(viewmethod(*args, **kwargs))
        if REFRESH_PAGE_SESSION_VAR in session and session[REFRESH_PAGE_SESSION_VAR]:
            resp.headers["HX-Refresh"] = 'true'
            session[REFRESH_PAGE_SESSION_VAR] = False
        return resp
    return new_viewmethod