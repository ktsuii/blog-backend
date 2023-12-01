from flask import request, render_template
from flask.views import MethodView

from apps.process_logic import ProcessLogic
from apps.spider.control import crawl_wallpaper, crawl_new_house


class WallpaperSpiderView(MethodView, ProcessLogic):

    def post(self, *args, **kwargs):
        body = request.json
        keyword = body.get('keyword', '')

        with self.session_maker() as session:
            result = crawl_wallpaper(session, self.crawler, keyword)

        return result


class NewHouseSpiderView(MethodView, ProcessLogic):

    def post(self, *args, **kwargs):
        body = request.json
        city = body.get('city', '')
        num = body.get('num', 1)
        is_async = body.get('craw_way', False)

        with self.session_maker() as session:
            result = crawl_new_house(session, self.crawler, city, num, is_async)

        return result


class SpiderIndexView(MethodView, ProcessLogic):

    def get(self, *args, **kwargs):
        return render_template('spider_index.html')