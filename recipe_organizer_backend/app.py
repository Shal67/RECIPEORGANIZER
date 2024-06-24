from flask import Flask
from extensions import db, migrate
from routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(main)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
