"""Rate limiting objects and decorators."""

from time import sleep
from typing import DefaultDict
from functools import wraps
from collections import defaultdict
from models import PermLevel
from flask import request
from security import get_api_key_or_raise, AuthorisationError
from local_settings import settings
import threading


rate_register: DefaultDict[str, int] = defaultdict(int)
"""Register of client IPs to the amount of requests received from them since
the last flush.
"""

_flush_loop_started = False


def _flush_register():
    rate_register.clear()

    if rate_limit_refresh := settings["RATE_LIMIT_REFRESH_HOURS"]:
        sleep_time = rate_limit_refresh * 60 * 60
    else:
        return
    
    while True:
        sleep(sleep_time)
        rate_register.clear()


def _start_flush_loop():
    threading.Thread(target=_flush_register).run()
    global _flush_loop_started
    _flush_loop_started = True


def rate_limited(func):
    """Decorator for routes that count towards the rate limit for requests by
    unauthenticated users.
    """
    
    @wraps(func)
    def wrapped(*args, **kwargs):
        user_ip = request.remote_addr
        
        try:
            apikey = get_api_key_or_raise()
        except AuthorisationError:
            apikey = None
        
        if apikey and apikey.level >= PermLevel.ADMIN:
            return func(*args, **kwargs)
        
        if apikey and apikey.level < PermLevel.ADMIN:
            limit = settings["USERS_RATE_LIMIT"]
        else:
            limit = settings["GUESTS_RATE_LIMIT"]
        
        if limit is None:
            return func(*args, **kwargs)
        
        if rate_register[user_ip] > limit:
            if refresh_time := settings["RATE_LIMIT_REFRESH_HOURS"]:
                refresh_time = f" {refresh_time} hours "
            
            return f"Rate limited. Authenticate, upgrade, or wait" \
                   f"{refresh_time or ' '}" \
                   f"to lift the limit.", 429
        
        rate_register[user_ip] += 1
        
        return func(*args, **kwargs)
    
    return wrapped


if not _flush_loop_started:
    _start_flush_loop()
