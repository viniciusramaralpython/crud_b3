from flask import Blueprint
from resources import register_user, login_user, get_users, get_user, update_user, delete_user


#Listando todas as rotas dos usuários
bp = Blueprint('api', __name__)

bp.add_url_rule('/register', 'register', register_user, methods=['POST'])
bp.add_url_rule('/login', 'login', login_user, methods=['POST'])
bp.add_url_rule('/users', 'get_users', get_users, methods=['GET'])
bp.add_url_rule('/user/<int:id>', 'get_user', get_user, methods=['GET'])
bp.add_url_rule('/user/<int:id>', 'update_user', update_user, methods=['PUT'])
bp.add_url_rule('/user/<int:id>', 'delete_user', delete_user, methods=['DELETE'])


#Quando o sistema estiver definido, abaixo vamos listar todas as rotas de funcionalidade do sistema