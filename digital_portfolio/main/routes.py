from flask import render_template, url_for, redirect, Blueprint, flash
from flask_login import current_user
from digital_portfolio.models import Portfolio

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    # if current_user.is_authenticated:
    #     if Portfolio.query.filter_by(current_user.username).first():
    #         flash('You have had a portfolio already')
    #         return redirect(url_for('users.user_portfolio'))
    return render_template('home.html')

@main.route("/about")
def about():
    return render_template('about.html', title='About')