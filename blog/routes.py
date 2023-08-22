from blog import app, db
from flask import render_template, redirect, url_for, flash
from blog.models import Post, User
from blog.forms import RegisterForm, LoginForm, PostForm
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/blog')
@login_required
def blog_page():
    posts = Post.query.all()
    return render_template('blog.html', posts=posts)


@app.route('/new-post', methods=['GET','POST'])
@login_required
def new_post_page():
    form = PostForm()
    if form.validate_on_submit():
        post_to_publish = Post(title=form.title.data,
                               text=form.text.data)
        db.session.add(post_to_publish)
        db.session.commit()
        return redirect(url_for('blog_page'))
    # if form.errors != {}:  # If no errors from validations
    #     for err_msg in form.errors.values():
    #         flash(f"There is a problem: {err_msg}", category='danger')
    return render_template('new-post.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email_address.data,
                              password_hash=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Your account has been created. You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('blog_page'))
    if form.errors != {}:  # If no errors from validations
        for err_msg in form.errors.values():
            flash(f"There is a problem: {err_msg}", category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('blog_page'))
        else:
            flash('Username or password is incorrect', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))
