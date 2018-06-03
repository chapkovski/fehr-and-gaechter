from channels.routing import route, route_class
from .consumers import TaskTracker

channel_routing = [
    route_class(TaskTracker, path=TaskTracker.url_pattern),

]