# import os
# from flask import Flask
# from src.controllers.auth_controller import auth_controller
# from src.controllers.home_controller import home_controller
# from src.middlewares.auth_middleware import auth_middleware
# from src.config.db_config import engine, Base
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # absolute path to 'src' folder
#
# app = Flask(
#     __name__,
#     static_folder=os.path.join(BASE_DIR, 'src/public'),
#     template_folder=os.path.join(BASE_DIR, 'views')
# )
#
# Base.metadata.create_all(bind=engine)
#
# app.register_blueprint(auth_controller)
# app.register_blueprint(home_controller)
#
# app.before_request(auth_middleware)
#
# if __name__ == '__main__':
#     app.run(debug=True, port=3000)


from dotenv import load_dotenv
from src.controllers.auth_controller import auth_controller
from src.controllers.home_controller import home_controller
from src.controllers.item_controller import item_controller  # import your blueprint
from src.middlewares.auth_middleware import auth_middleware
from src.config.db_config import engine, Base
import os
from flask import Flask
from src.controllers.auth_controller import auth_controller
from src.controllers.home_controller import home_controller
from src.middlewares.auth_middleware import auth_middleware
from src.config.db_config import engine, Base
from flask import g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # absolute path to project root

load_dotenv()

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'src/public'),
    template_folder=os.path.join(BASE_DIR, 'views')
)


@app.context_processor
def inject_user():
    return dict(is_authenticated=getattr(g, 'is_authenticated', False))


app.secret_key = os.getenv('JWT_SECRET')

Base.metadata.create_all(bind=engine)

# Register blueprints AFTER app creation
app.register_blueprint(auth_controller)
app.register_blueprint(home_controller)
app.register_blueprint(item_controller)  # register item_controller routes

app.before_request(auth_middleware)

if __name__ == '__main__':
    app.run(debug=True, port=3000)


