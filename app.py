# -*- coding: utf-8 -*-
from flask import Flask

import config as _config
from views import general


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(_config)

    app.register_blueprint(general.bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
