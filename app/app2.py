from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize extensions
db.init_app(app)

# Flask-Admin setup
admin = Admin(app, name='My Admin', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))

@app.route('/')
def home():
    return '<h1>Welcome to the Flask App!</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates database tables 
    app.run(debug=True)

