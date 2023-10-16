from apps.checker.views import (HealthCheckView)
from apps.spider.views import (WallpaperSpiderView)

url_patterns = [
    # (url, view, endpoint, methods)
    ('/ping', HealthCheckView, 'health-check', ['GET']),
    ('/spider/wallpaper', WallpaperSpiderView, 'wallpaper-download', ['POST']),
]
