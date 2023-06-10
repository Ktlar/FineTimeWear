from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from FineWatches.queries import get_user_by_user_name, get_brandrep_by_pk, get_customer_by_pk
from FineWatches.utils.choices import WatchModelChoices, WatchBrandChoices, UserTypeChoices, \
    WatchCaseMaterialChoices, WatchStrapMaterialChoices, WatchMovementTypeChoices, WatchWaterResistanceChoices, \
    WatchCaseDiameterChoices, WatchCaseThicknessChoices, WatchBandWidthChoices, WatchDialColorChoices, \
    WatchCrystalMaterialChoices, WatchComplicationChoices, WatchPowerReserveChoices


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


class FilterWatchForm(FlaskForm):
    category = SelectField('Brand',
                           choices=WatchBrandChoices.choices())
    item = SelectField('Model',
                       choices=WatchModelChoices.choices())
    sold_by = StringField('Sold by')
    price = FloatField('Price (lower than or equal to)',
                       validators=[NumberRange(min=0, max=100000)])
    submit = SubmitField('Filter')


class AddWatchForm(FlaskForm):
    category = SelectField('Brand',
                        validators=[DataRequired()],
                        choices=WatchBrandChoices.choices())
    item = SelectField('Model',
                       validators=[DataRequired()],
                       choices=WatchModelChoices.choices())
    variety = SelectField('Case material',
                          validators=[DataRequired()],
                          choices=WatchCaseMaterialChoices.choices())
    unit = SelectField('Strap material',
                       validators=[DataRequired()],
                       choices=WatchStrapMaterialChoices.choices())
    unit = SelectField('Water resistance',
                       validators=[DataRequired()],
                       choices=WatchWaterResistanceChoices.choices())
    unit = SelectField('Movement type',
                       validators=[DataRequired()],
                       choices=WatchMovementTypeChoices.choices())
    unit = SelectField('Case diameter',
                       validators=[DataRequired()],
                       choices=WatchCaseDiameterChoices.choices())
    unit = SelectField('Case thickness',
                       validators=[DataRequired()],
                       choices=WatchCaseThicknessChoices.choices())
    unit = SelectField('Band width',
                       validators=[DataRequired()],
                       choices=WatchBandWidthChoices.choices())
    unit = SelectField('Dial Color',
                       validators=[DataRequired()],
                       choices=WatchDialColorChoices.choices())
    unit = SelectField('Crystal material',
                       validators=[DataRequired()],
                       choices=WatchCrystalMaterialChoices.choices())
    unit = SelectField('Complications',
                       validators=[DataRequired()],
                       choices=WatchComplicationChoices.choices())
    unit = SelectField('Power reserve',
                       validators=[DataRequired()],
                       choices=WatchPowerReserveChoices.choices())
    price = IntegerField('Price',
                         validators=[DataRequired(), NumberRange(min=0, max=100000)])
    brandrep = IntegerField('Brand representative',
                             validators=[DataRequired()],
                             render_kw=dict(disabled='disabled'))
    submit = SubmitField('Add watch')


    def validate_price(self, field):
        farmer = get_brandrep_by_pk(self.brandrep_pk.data)
        if farmer is None:
            raise ValidationError("You need to be an established brand to sell watches here")


class BuyWatchForm(FlaskForm):
    submit = SubmitField('Buy')

    def validate_submit(self, field):
        customer = get_customer_by_pk(current_user.pk)
        if not customer:
            raise ValidationError("You need to be a customer buy watches.")

class RestockWatchForm(FlaskForm):
    submit = SubmitField('Restock')

