from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///My.db'  # Change this as needed
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session management
db = SQLAlchemy(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and user.password == data['password']:
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        return 'Invalid credentials!', 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        new_user = User(username=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')  # Ensure this points to your index.html

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))  # Redirect to login after logout

@app.route('/transactions', methods=['POST', 'GET'])
@login_required
def manage_transactions():
    if request.method == 'POST':
        data = request.get_json()
        new_transaction = Transaction(
            user_id=current_user.id,
            amount=data['amount'],
            description=data['description'],
            type=data['type']
        )
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction added!'}), 201

    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': t.id, 'amount': t.amount, 'description': t.description, 'type': t.type} for t in transactions])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables within the application context
    app.run(debug=True)
