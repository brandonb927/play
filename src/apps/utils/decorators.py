from django.core.exceptions import PermissionDenied


def superuser_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_superuser:
            return function(request, *args, **kwargs)
        raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
