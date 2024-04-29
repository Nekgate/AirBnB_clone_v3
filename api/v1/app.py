#!/usr/bin/python3
"""
Creating a flask app, register the blueprint app_viewss
-to flask instantiated app
Then handles our api
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appconetxt
def teardown_engine(exception):
    """
    Creating a teardown engint
    Defining our app's blue print
    close storage
    """
    storage.close()

    @app.errorhandler(404)
    def not_found(error):
        """
        Handling errors if something is not found
        returning json for errors in requests
        removing default
        """
        response = {"error": "Not found"}
        return jsonify(response), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(debug=True, hosts=HOST, port=PORT, threaded=True)
