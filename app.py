from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from api.search import search_bp
from api.categories import categories_bp
from api.analyze import analyze_bp
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

app.register_blueprint(search_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(analyze_bp)


@app.route("/")
@app.route("/<path:path>")
def index(path=""):
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
