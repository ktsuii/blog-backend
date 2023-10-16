from flask.views import MethodView

from apps.process_logic import ProcessLogic


class HealthCheckView(MethodView, ProcessLogic):

    def get(self, *args, **kwargs):
        return 'pong'
