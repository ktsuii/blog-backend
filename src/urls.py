from api.checker.views import (HealthCheckView)

url_patterns = [
    # (url, view, endpoint, methods)
    ('/ping', HealthCheckView, 'health-check', ['GET']),
]
