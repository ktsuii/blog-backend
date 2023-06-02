from flask.views import MethodView


class HealthCheckView(MethodView):

    def get(self, *args, **kwargs):
        return 'pong'
