import os
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'dev')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run()