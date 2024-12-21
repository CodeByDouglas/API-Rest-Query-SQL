from flask import Flask
from app.config import Config
from app.controllers.user_controller import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix="/api")
app.config.from_object(Config)

@app.route('/')
def home():
    return "API Flask funcionando!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
