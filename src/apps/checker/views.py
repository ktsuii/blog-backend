from flask.views import MethodView

from apps.process import ProcessLogic


class HealthCheckView(MethodView, ProcessLogic):

    def get(self, *args, **kwargs):
        with self.session_maker() as session:
            ...
            return 'pong'
