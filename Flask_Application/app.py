from flask import Flask
from controllers.routes import routes
from config import MAX_CONTENT_LENGTH, SECRET_KEY, UPLOAD_FOLDER


app = Flask(__name__)


app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["SECRET_KEY"] = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)