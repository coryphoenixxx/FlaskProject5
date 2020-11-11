from wtforms import IntegerField, StringField, SubmitField, PasswordField, validators
from flask_wtf import FlaskForm


class DishForm(FlaskForm):
     dish_id = IntegerField()
     category = StringField()
     submit = SubmitField()


class RegistrationForm(FlaskForm):
     email = StringField("Электропочта:",
                         [validators.DataRequired(),
                          validators.Length(min=6, max=32, message="Почта должна быть не менее 6 символов"),
                          validators.Email(message='Некорректная почта')],
                         render_kw={'autofocus': True})
     password = PasswordField("Пароль:",
                              [validators.DataRequired(),
                               validators.Length(min=8, max=32, message="Пароль должен быть не менее 8 символов"),
                               validators.EqualTo('confirm', message="Пароли не совпадают")])
     confirm = PasswordField("Повторите пароль:", [validators.DataRequired()])
     submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
     email = StringField("Электропочта:", [validators.DataRequired()], render_kw={'autofocus': True})
     password = PasswordField("Пароль:", [validators.DataRequired()])
     submit = SubmitField("Войти")


class OrderForm(FlaskForm):
    username = StringField("Ваше имя", [validators.DataRequired()], render_kw={'autofocus': True})
    addr = StringField("Ваш адрес", [validators.DataRequired()])
    phone = StringField("Ваш телефон", [validators.DataRequired()])
    submit = SubmitField("Оформить заказ")