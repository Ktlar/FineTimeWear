from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user

from FineWatches.forms import UserLoginForm, UserSignupForm
from FineWatches.models import BrandRep, Customer
from FineWatches.queries import get_user_by_user_name, insert_brandrep, insert_customer
from FineWatches.utils.choices import UserTypeChoices

Login = Blueprint('Login', __name__)


@Login.route("/")
@Login.route("/index.html")
def index():
    return render_template('index.html')


@Login.route("/about.html")
def about():
    return render_template('about.html')


@Login.route("/omega.html")
def omega():
    return render_template('omega.html')

@Login.route("/patek.html")
def patek():
    return render_template('patek.html')

@Login.route("/rolex.html")
def rolex():
    return render_template('rolex.html')


@Login.route("/login.html", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Login.index.html'))
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user_by_user_name(form.user_name.data)
            if user and user['password'] == form.password.data:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Login.index.html'))
    return render_template('login.html', form=form)


@Login.route("/signup.html", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('Login.index'))
    form = UserSignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_data = dict(full_name=form.full_name.data,
                             user_name=form.user_name.data,
                             password=form.password.data)
            if form.user_type.data == UserTypeChoices.values()[0]:
                brandrep = BrandRep(user_data)
                insert_brandrep(brandrep)
            elif form.user_type.data == UserTypeChoices.values()[1]:
                customer = Customer(form.data)
                insert_customer(customer)
            user = get_user_by_user_name(form.user_name.data)
            if user:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Login.home'))
    return render_template('signup.html', form=form)


@Login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Login.login'))
