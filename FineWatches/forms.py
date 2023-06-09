"""The forms.py file contains several Flask forms that are used for user input validation and rendering 
in the GreenGroceries web application. Let's go through each form and explain its purpose and fields:

UserLoginForm:

Purpose: This form is used for user login.
Fields:
user_name: StringField to enter the username.
password: PasswordField to enter the password.
submit: SubmitField to submit the login form.
Validation:
validate_password: Validates the entered password against the user's stored password in the database.
UserSignupForm:

Purpose: This form is used for user registration.
Fields:
full_name: StringField to enter the user's full name.
user_name: StringField to enter the username.
password: PasswordField to enter the password.
password_repeat: PasswordField to repeat and confirm the password.
user_type: SelectField to choose the user type.
submit: SubmitField to submit the signup form.
Validation:
validate_user_name: Validates that the entered username is not already in use.
validate_password_repeat: Validates that the entered passwords match.
FilterProduceForm:

Purpose: This form is used for filtering produce items.
Fields:
category: SelectField to choose the produce category for filtering.
item: SelectField to choose the produce item (subcategory) for filtering.
variety: SelectField to choose the produce variety for filtering.
sold_by: StringField to enter the name of the seller for filtering.
price: FloatField to enter the maximum price for filtering.
submit: SubmitField to submit the filter form.
AddProduceForm:

Purpose: This form is used for adding produce items.
Fields:
category: SelectField to choose the produce category.
item: SelectField to choose the produce item (subcategory).
variety: SelectField to choose the produce variety.
unit: SelectField to choose the produce unit.
price: IntegerField to enter the produce price.
farmer_pk: IntegerField (disabled) to display the farmer's primary key.
submit: SubmitField to submit the add produce form.
Validation:
validate_price: Validates that the entered price is within a specific range based on the farmer's primary key.
BuyProduceForm:

Purpose: This form is used for confirming the purchase of produce.
Fields:
submit: SubmitField to confirm the purchase.
Validation:
validate_submit: Validates that the current user is a customer before allowing the purchase.
RestockProduceForm:

Purpose: This form is used for confirming the restocking of produce.
Fields:
submit: SubmitField to confirm the restocking.
These forms provide a way to handle user input, perform validation checks, 
and render the necessary fields in the corresponding Flask views or templates within the GreenGroceries web application."""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from GreenGroceries.queries import get_user_by_user_name, get_farmer_by_pk, get_customer_by_pk
from GreenGroceries.utils.choices import ProduceItemChoices, ProduceCategoryChoices, UserTypeChoices, \
    ProduceVarietyChoices, ProduceUnitChoices


class UserLoginForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    submit = SubmitField('Login')

    def validate_password(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user is None:
            raise ValidationError(f'User name "{self.user_name.data}" does not exist.')
        if user.password != self.password.data:
            raise ValidationError(f'User name or password are incorrect.')


class UserSignupForm(FlaskForm):
    full_name = StringField('Full name',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Full name'))
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    password_repeat = PasswordField('Repeat Password',
                                    validators=[DataRequired()],
                                    render_kw=dict(placeholder='Password'))
    user_type = SelectField('User type',
                            validators=[DataRequired()],
                            choices=UserTypeChoices.choices())
    submit = SubmitField('Sign up')

    def validate_user_name(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user:
            raise ValidationError(f'User name "{self.user_name.data}" already in use.')

    def validate_password_repeat(self, field):
        if not self.password.data == self.password_repeat.data:
            raise ValidationError(f'Provided passwords do not match.')


class FilterProduceForm(FlaskForm):
    category = SelectField('Category',
                           choices=ProduceCategoryChoices.choices())
    item = SelectField('Item',
                       choices=ProduceItemChoices.choices())
    variety = SelectField('Variety',
                          choices=ProduceVarietyChoices.choices())
    sold_by = StringField('Sold by')
    price = FloatField('Price (lower than or equal to)',
                       validators=[NumberRange(min=0, max=100)])

    submit = SubmitField('Filter')


class AddProduceForm(FlaskForm):
    category = SelectField('Category',
                           validators=[DataRequired()],
                           choices=ProduceCategoryChoices.choices())
    item = SelectField('Item (Subcategory)',
                       validators=[DataRequired()],
                       choices=ProduceItemChoices.choices())
    variety = SelectField('Variety',
                          validators=[DataRequired()],
                          choices=ProduceVarietyChoices.choices())
    unit = SelectField('Unit',
                       validators=[DataRequired()],
                       choices=ProduceUnitChoices.choices())
    price = IntegerField('Price',
                         validators=[DataRequired(), NumberRange(min=0, max=100)])
    farmer_pk = IntegerField('Farmer',
                             validators=[DataRequired()],
                             render_kw=dict(disabled='disabled'))
    submit = SubmitField('Add produce')

    def validate_price(self, field):
        farmer = get_farmer_by_pk(self.farmer_pk.data)
        if farmer is None:
            raise ValidationError("You need to be a farmer to sell produce!")


class BuyProduceForm(FlaskForm):
    submit = SubmitField('Yes, buy it')

    def validate_submit(self, field):
        customer = get_customer_by_pk(current_user.pk)
        if not customer:
            raise ValidationError("You must be a customer in order to create orders.")


class RestockProduceForm(FlaskForm):
    submit = SubmitField('Yes, restock it')

    hey