
#Congigurações do banco de dados com a utilização de SQL Alchemy
#Essa interface permite que conectemos bancos mais robustos no futuro sem grandes alterações 
class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'superjwtsecretkey'
