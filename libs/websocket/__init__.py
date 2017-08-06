import django.conf.urls


def url(regex, view, kwargs=None, name=None, method=None):
    if not method:
        method = 'http.request'
    if not kwargs:
        kwargs = {}
    kwargs['method'] = method
    return django.conf.urls.url(regex, view, kwargs, name)
