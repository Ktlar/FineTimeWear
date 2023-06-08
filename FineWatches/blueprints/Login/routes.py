"""The routes.py file in Flask is responsible for defining the routes (URL endpoints) and corresponding view functions
 for your application. It handles the incoming requests from clients and determines which function to execute to generate
   the appropriate response.

Let's go through the code in routes.py and explain each section:

The imports at the top import the necessary modules and functions from Flask and other project files.

The Login blueprint is created using Blueprint('Login', __name__). This blueprint is used to group related routes and views together.
 It allows for modular organization and easy registration of the blueprint in the main Flask application.

The home(), about(), and style_guide() functions are view functions associated with specific routes. 
They use the render_template() function to render the corresponding HTML templates for these routes. 
For example, when a user visits the /home route, the home() function is executed and the pages/home.html template is rendered and returned.

The login() function is associated with the /login route and handles both GET and POST requests.
 It checks if the user is already authenticated (logged in). If the user is authenticated, they are redirected to the home page.
   If not, the UserLoginForm form is instantiated. On a POST request, the form is validated.
     If the validation succeeds, the user's credentials are checked, and if they are correct, the user is logged in using the login_user() 
     function from Flask-Login. The next_page variable is used to redirect the user to the next page after successful login.

The signup() function handles the /signup route and also handles both GET and POST requests. Similar to the login() function,
 it checks if the user is already authenticated. On a POST request, the UserSignupForm form is instantiated and validated. Depending on the user type selected in the form, either a Farmer or Customer instance is created and inserted into the database using the appropriate function (insert_farmer() or insert_customer()). After successful signup, the user is logged in and redirected to the home page.

The logout() function is associated with the /logout route. 
It simply logs out the current user using logout_user() from Flask-Login and redirects them to the login page.

Overall, routes.py defines the routes and view functions for the different pages and functionalities of your luxury watches application.
 It handles user authentication, rendering of templates, form validation, and user registration."""
from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user

from GreenGroceries.forms import UserLoginForm, UserSignupForm
from GreenGroceries.models import Farmer, Customer
from GreenGroceries.queries import get_user_by_user_name, insert_farmer, insert_customer
from GreenGroceries.utils.choices import UserTypeChoices

Login = Blueprint('Login', __name__)


@Login.route("/")
@Login.route("/home")
def home():
    return render_template('pages/home.html')


@Login.route("/about")
def about():
    return render_template('pages/about.html')


@Login.route("/style-guide")
def style_guide():
    return render_template('pages/style-guide.html')


@Login.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user_by_user_name(form.user_name.data)
            if user and user['password'] == form.password.data:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Login.home'))
    return render_template('pages/login.html', form=form)


@Login.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = UserSignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_data = dict(full_name=form.full_name.data,
                             user_name=form.user_name.data,
                             password=form.password.data)
            if form.user_type.data == UserTypeChoices.values()[0]:
                farmer = Farmer(user_data)
                insert_farmer(farmer)
            elif form.user_type.data == UserTypeChoices.values()[1]:
                customer = Customer(form.data)
                insert_customer(customer)
            user = get_user_by_user_name(form.user_name.data)
            if user:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Login.home'))
    return render_template('pages/signup.html', form=form)


@Login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Login.login'))
