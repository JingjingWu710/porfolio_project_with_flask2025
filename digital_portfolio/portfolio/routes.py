from flask import (render_template, url_for, flash, redirect, \
    request, abort, Blueprint)
from flask_login import current_user, login_required
from digital_portfolio import db
from digital_portfolio.models import Portfolio, Comments
from digital_portfolio.portfolio.forms import PorfolioForm
from datetime import datetime

portfolio = Blueprint('portfolio', __name__)

@portfolio.route("/create_portfolio", methods=['Get','POST'])
def create_portfolio():
    if current_user.is_authenticated:
        if Portfolio.query.filter_by(author=current_user).first():
            flash('You have had a portfolio already', 'info')
            return redirect(url_for('users.user_portfolio', username=current_user.username))
    else:
        flash('You should log in first.', 'info')
        return redirect(url_for('users.login'))
    form = PorfolioForm()
    if form.validate_on_submit():
        portfolio = Portfolio(name=form.name.data, \
            tech_skills=form.tech_skills.data, \
                work_produced=form.work_produced.data, \
                    experience=form.experience.data, \
                        contact=form.contact.data, \
                            author=current_user)
        db.session.add(portfolio)
        db.session.commit()
        flash('Your portfolio has been created!', 'success')
        return redirect(url_for('users.user_portfolio', username=current_user.username))
    return render_template('create_portfolio.html', title='Create a portfolio', 
                           form=form, legend='Create Your Portfolio!')
    
@portfolio.route("/<string:username>/delete", methods=['POST'])
@login_required
def delete_portfolio(username):
    portfolio = Portfolio.query.filter_by(author=current_user).first_or_404()
    if portfolio.author.username != username: 
        abort(403)
    Comments.query.filter_by(portfolio_id=portfolio.id).delete()
    db.session.delete(portfolio)
    db.session.commit()
    flash('Your portfolio has been deleted. You can create a new one now.', 'success')
    return redirect(url_for('main.home'))

@portfolio.route("/<string:username>/edit", methods=['GET', 'POST'])
@login_required
def edit_portfolio(username):
    portfolio = Portfolio.query.filter_by(author=current_user).first_or_404()
    if portfolio.author.username != username:
        abort(403)
    update = PorfolioForm()
    if update.validate_on_submit(): 
        portfolio.name = update.name.data
        portfolio.contact = update.contact.data
        portfolio.tech_skills = update.tech_skills.data
        portfolio.work_produced = update.work_produced.data
        portfolio.experience = update.experience.data
        portfolio.date_edited = datetime.now()
        db.session.commit()
        flash('Your portfolio has been updated', 'success')
        return redirect(url_for('users.user_portfolio', username=username))
    elif request.method == 'GET':
        update.name.data =  portfolio.name
        update.contact.data = portfolio.contact
        update.tech_skills.data = portfolio.tech_skills
        update.work_produced.data = portfolio.work_produced
        update.experience.data = portfolio.experience
    return render_template('create_portfolio.html', title='Edit the Portfolio',
                           form=update, legend='Edit the Portfolio')

