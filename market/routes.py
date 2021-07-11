from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask import render_template, redirect, url_for, flash, request


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.purchase(current_user)
                flash(f"Item purchased! You purchased { p_item_object.name} \
                    for {p_item_object.price}!", category="success")
            else:
                flash(f"You don't have enough budget to buy \
                    { p_item_object.name }!", category="danger")
        else:
            flash("Item is no longer available!", category="danger")
        # Selling Logic
        sold_item = request.form.get('selling_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"{s_item_object.name} placed on the market for \
                    {s_item_object.price}!", category="success")
            else:
                flash(f"You cannot sell { p_item_object.name }!",
                      category="danger")
        else:
            flash("Item is no longer available!", category="danger")
        return redirect(url_for('market_page'))
    else:
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form,
                               selling_form=selling_form, owned_items=owned_items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Account successfully created! You are logged in as {user_to_create.username}!',
              category='success')
        login_user(user_to_create)
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for error in form.errors.values():
            # Index 0 for error as error is stored as a list
            flash(f'The following error has occured: {error[0]}',
                  category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user:
            if attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash(f'Welcome back! Hi {attempted_user.username}!',
                      category='success')
                return redirect(url_for('market_page'))
            else:
                flash('Password is incorrect for username!', category='danger')
        else:
            flash('User does not exist!', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Thank you for visiting our site! You have been logged out!',
          category='info')
    return redirect(url_for('home_page'))
