from flask import Flask
from flask_cors import CORS
from settings import Config
from urls import url_patterns
from typing import Type, List
from flask.views import MethodView

app = Flask(Config.PROJECT_NAME, template_folder=Config.TemplatePath)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)


def register_api(
        url: str,
        view: Type[MethodView],
        endpoint: str,
        methods: List[str] = None,
        prefix='/api',
):
    app.add_url_rule(
        rule=f'{prefix}{url}',
        view_func=view.as_view(endpoint),
        methods=methods or ['POST'],
    )


for url_info in url_patterns:
    register_api(*url_info)
