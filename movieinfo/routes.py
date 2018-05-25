from movieinfo import app, db, bcrypt
from movieinfo.movie import movie_db
from flask import render_template, url_for, redirect, flash, request
from movieinfo.forms import Search, RegistrationForm, LoginForm
from movieinfo.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=['GET', 'POST'])
def hello():
    return redirect(url_for('home'))


@app.route("/home", methods=['GET', 'POST'])
def home():
    form = Search()
    if form.validate_on_submit():
        movie_list = movie_db(form.moviename.data)
        return render_template('home.html', form=form, movie_list=movie_list)
    return render_template('home.html', form=form)


'''movie_list = movie_db("ant")
for movie in movie_list:
    print(movie["title"])
    print(img_path(movie['backdrop_path']))
'''


@app.route("/wishlist")
@login_required
def wishlist():
    return render_template('wishlist.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('form is validated', 'success')
            login_user(user, True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
