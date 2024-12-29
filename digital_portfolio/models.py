from datetime import datetime
from digital_portfolio import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    portfolio = db.relationship('Portfolio', backref='author', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_edited = db.Column(db.DateTime, nullable=False, default=datetime.now)
    tech_skills = db.Column(db.Text, nullable=False)
    work_produced = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    comment = db.relationship('Comments', backref='portfolio', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Portfolio('{self.name}', '{self.date_edited}')"
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    comment_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)