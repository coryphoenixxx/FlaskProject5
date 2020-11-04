import json
from flask import render_template, session, redirect, request, flash
from werkzeug.security import check_password_hash

from app import app, db
from models import Category, Dish, User, Order
from forms import DishForm, LoginForm, RegistrationForm, OrderForm
from mail import send_order_mail


@app.route('/', methods=['GET', 'POST'])
def render_main():
    try:
        cart = session.get('cart', {'total_cost': 0, 'dishes_list': []})
        session['cart'] = cart

        form = DishForm()
        if request.method == 'POST':
            id = form.dish_id.data
            dish = db.session.query(Dish).get(id)
            cart['total_cost'] += dish.price
            cart['dishes_list'].append(id)
            session['cart'] = cart
            return redirect('/')

        categories = db.session.query(Category).order_by(Category.id.desc()).all()
        return render_template('main.html', cats=categories, cart=cart, form=form, email=session.get('email', False))
    except Exception as err:
        print(str(err))
        return redirect('/500/')


@app.route('/cart/', methods=['GET', 'POST'])
def render_cart():
    cart = session.get('cart', {'total_cost': 0, 'dishes_list': []})
    session['cart'] = cart

    dish_form = DishForm()
    order_form = OrderForm()

    if order_form.validate_on_submit():
        order = Order(total=session['cart']['total_cost'],
                      status="в процессе",
                      username=order_form.username.data,
                      phone=order_form.phone.data,
                      addr=order_form.addr.data,
                      email=session['email'],
                      dishes=json.dumps(session['cart']['dishes_list']),
                      user=db.session.query(User).filter_by(email=session['email']).first()
                      )
        db.session.add(order)
        db.session.commit()

        dish_titles = [db.session.query(Dish).get(id).title for id in session['cart']['dishes_list']]
        send_order_mail(order.email, order.username, dish_titles)

        session.pop('cart')
        return render_template('ordered.html')

    if request.method == 'POST':
        id = dish_form.dish_id.data
        dish = db.session.query(Dish).get(id)
        cart['total_cost'] -= dish.price
        cart['dishes_list'].pop(cart['dishes_list'].index(id))
        flash("Блюдо удалено из корзины")
        return redirect('/cart/')

    dishes = {}
    for id in cart['dishes_list']:
        dish = db.session.query(Dish).get(id)
        if dish in dishes:
            dishes[dish] += 1
        else:
            dishes[dish] = 1

    email = session.get('email', False)
    uinfo = ['', '', '']
    if email:
        last_order = db.session.query(User).filter_by(email=email).first().orders[::-1]
        if last_order:
            uinfo = [last_order[0].username, last_order[0].addr, last_order[0].phone]

    return render_template('cart.html', dish_form=dish_form, order_form=order_form, dishes=dishes, cart=cart, email=session.get('email', False), uinfo=uinfo)


@app.route('/registration/', methods=['GET', 'POST'])
def render_registration():
    if session.get('email'):
        return redirect("/")

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.email.data, form.password.data)
        is_user = db.session.query(User).filter_by(email=user.email).first()
        if is_user:
            flash("Пользователь с указанной почтой уже существует")
            return render_template('registration.html', form=form)
        db.session.add(user)
        db.session.commit()
        session['email'] = user.email
        flash("Вы успешно зарегистрированы!", category='success')
        is_cart = session.get('cart', {'total_cost': 0, 'dishes_list': []})['total_cost']
        return render_template('registration.html', form=form, is_cart=is_cart)

    return render_template('registration.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def render_login():
    if session.get('email'):
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['email'] = email
            return redirect('/')
        flash("Неверная почта или пароль")
        return redirect('/login/')

    return render_template('login.html', form=form)


@app.route('/logout/')
def render_logout():
    if session.get("email"):
        session.pop('cart')
        session.pop('email')
    return redirect('/login/')


@app.route('/account/')
def render_account():
    if not session.get('email'):
        return redirect("/login/")

    user = db.session.query(User).filter_by(email=session.get('email')).first()
    uorders = []
    for o in user.orders[::-1]:
        order = {'date': o.date.date().strftime('%d %B'),
                 'total': o.total,
                 'status': o.status,
                 'dishes': []}
        ids = json.loads(o.dishes)
        for id in ids:
            d = db.session.query(Dish).get(id)
            dish = {}
            dish['title'] = d.title
            dish['amount'] = ids.count(id)
            dish['cost'] = dish['amount'] * d.price
            if dish not in order['dishes']:
                order['dishes'].append(dish)
        uorders.append(order)

    return render_template('account.html',
                           cart=session.get('cart', {'total_cost': 0, 'dishes_list': []}),
                           email=session.get('email', False),
                           orders=uorders)


@app.errorhandler(404)
def page_404(e):
    return render_template('404.html', error=e), 404

@app.route('/500/')
def page_500():
    err = session.get('err')
    return err

