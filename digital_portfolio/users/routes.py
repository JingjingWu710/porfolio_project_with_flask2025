from flask import render_template, url_for, flash, redirect, request, Blueprint
from digital_portfolio import db, bcrypt
from digital_portfolio.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from digital_portfolio.portfolio.forms import CommentForm
from digital_portfolio.models import User, Portfolio, Comments
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in and make your portfolio', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Login Unseccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)
    
@users.route("/portfolio/<string:username>", methods=['GET','POST'])
def user_portfolio(username):
    user = User.query.filter_by(username=username).first_or_404()
    portfolio = Portfolio.query.filter_by(author=user).first()
    if portfolio is None:
        flash('Please create one portfolio first', 'warning')
        return redirect(url_for('portfolio.create_portfolio'))
    comments = Comments.query.filter_by(portfolio_id=portfolio.id).order_by(Comments.comment_time.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        if form.content.data:
            if current_user.is_authenticated:
                comment = Comments(content=form.content.data, portfolio_id=portfolio.id, username=current_user.username)
                db.session.add(comment)
                db.session.commit()
                flash('Your comment has been send.', 'success')
                return redirect(url_for('users.user_portfolio', username=username))
            else:
                flash('You must log in first!', 'danger')
                return redirect(url_for('users.login'))
        else:
            form.content.errors.append('Comment content cannot be empty!')
    return render_template('user_portfolio.html', portfolio=portfolio, 
                           comments=comments, form=form)

