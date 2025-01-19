from flask import Flask
from app.routes import main as routes
from flask_cors import CORS

app = Flask(__name__)

# Configuration des paramètres de l'application
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

# Enregistrement des routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)