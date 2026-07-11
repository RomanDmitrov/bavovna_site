from functools import wraps
from django.core.cache import cache
from django.shortcuts import redirect


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def throttle_post(key_prefix, seconds=60, redirect_to=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.method == 'POST':
                ip = get_client_ip(request)
                cache_key = f'throttle:{key_prefix}:{ip}'

                if cache.get(cache_key):
                    if redirect_to:
                        return redirect(redirect_to)
                    return redirect(request.path)

                cache.set(cache_key, True, timeout=seconds)

            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
