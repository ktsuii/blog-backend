from flask import request
from flask.views import MethodView

from apps.process_logic import ProcessLogic
from apps.spider.control import crawl_wallpaper


class WallpaperSpiderView(MethodView, ProcessLogic):

    def post(self, *args, **kwargs):
        body = request.json
        keyword = body.get('keyword', '')

        with self.session_maker() as session:
            result = crawl_wallpaper(session, self.crawler, keyword)

        return result
