from flask import Flask
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_login import current_user

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    mysql.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor, inicia sesión para continuar."
    login_manager.init_app(app)



# Importa y registra blueprints
    from .routes.auth_routes import auth_bp, User
    from .routes.main_routes import main_bp
    from .routes.productos_routes import productos_bp
    from .routes.usuarios_routes import usuarios_bp
    from .routes.ventas_admin_routes import ventas_admin_bp
    from .routes.carrito_routes import carrito_bp


    # Registro de blueprints (una sola vez cada uno)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(ventas_admin_bp)
    app.register_blueprint(carrito_bp)


    
            
    

    @login_manager.user_loader
    def load_user(user_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, role FROM usuarios WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        if user:
            return User(user[0], user[1], user[2])
        return None
    
    @app.context_processor
    def inject_user_role():
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            return {
                'rol': getattr(current_user, 'role', None),
                'current_user': current_user
            }
        return {
            'rol': None,
            'current_user': None
        }
        
    @app.context_processor
    def inject_user_data():
        if current_user.is_authenticated:
            return {'user': current_user, 'tema_usuario': getattr(current_user, 'tema', 'oscuro')}
        return {'user': None, 'tema_usuario': 'oscuro'}
    



    return app
