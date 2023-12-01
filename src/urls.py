from apps.checker.views import (HealthCheckView)
from apps.spider.views import (WallpaperSpiderView, SpiderIndexView, NewHouseSpiderView)

url_patterns = [
    # (url, view, endpoint, methods)
    ('/ping', HealthCheckView, 'health-check', ['GET']),
    ('/spider/index', SpiderIndexView, 'spider-index', ['GET']),
    ('/spider/wallpaper', WallpaperSpiderView, 'wallpaper-download', ['POST']),
    ('/spider/new-house', NewHouseSpiderView, 'new-house-download', ['POST']),
]
