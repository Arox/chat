from django.conf.urls import include, RegexURLResolver, RegexURLPattern
from channels.routing import route
from libs.websocket import url


urlpatterns = [
    url(r'^/room/', include('room.websocket_urls'))
]


def calc_routes(url_list, parent_pattern = None):
    result = []
    if parent_pattern is None:
        parent_pattern = ''
    for url_path in url_list:
        if isinstance(url_path, RegexURLResolver):
            result += calc_routes(url_path.url_patterns, '{0}{1}'.format(parent_pattern, url_path.regex.pattern))
        elif isinstance(url_path, RegexURLPattern):
            result.append(route(url_path.default_args['method'],
                                url_path.callback,
                                path='{0}{1}'.format(parent_pattern, url_path.regex.pattern).replace('//', '/')))
    return result


routing = [i for i in calc_routes(urlpatterns)]
