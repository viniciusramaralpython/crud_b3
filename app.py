from flask import Flask
from config import Config
from models import db
from routes import bp as api_bp
from flask_jwt_extended import JWTManager


#Instanciando o Flask
app = Flask(__name__)
app.config.from_object(Config)

#Iniciando o banco de dados SQLite
db.init_app(app)

#Iniciando o JWT para auxiliar na segurança
jwt = JWTManager(app)

#Gerenciando os endereços da API 
app.register_blueprint(api_bp, url_prefix='/api')

#Criando o banco de dados
with app.app_context():
    db.create_all()


#Executando a aplicação
if __name__ == '__main__':
    app.run(debug=True)
