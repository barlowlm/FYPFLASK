import secrets
from PIL import Image
from flask import escape, request, render_template, redirect, url_for, flash, request, abort
from flaskd3.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskd3.models import User, Post
from flaskd3 import app, db, brcypt, mail
from flask_login import login_user,logout_user , current_user, login_required
from flask_mail import Message

import os
import json
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
import pygal

#print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(1438094031))


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
dropzone = Dropzone(app)


def create_app(config):
    app = Flask(__name__)
    dropzone.init_app(app)
    return app

@app.route('/', methods=["GET","POST"])
@app.route('/home', methods=["GET","POST"])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.htm', posts=posts)


@app.route('/about')
def about():
    #name = request.args.get("name", "World")
    #return "<h1>About Page!</h1>"#f'Hello, {escape(name)}!'
    return render_template('about.htm')

target = os.path.join(APP_ROOT, 'data/')

@app.route('/upload', methods=['GET','POST'])
def upload():

    if not os.path.isdir(target):
       os.mkdir(target)

    if request.method == 'POST':
        f = request.files.get('file')
        try:
            f.save(os.path.join(target, f.filename))
        except Exception:
            print("FilesSavedIndividually")
           
    return render_template('upload.htm')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=brcypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email= form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has now been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.htm', title='Register', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and brcypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("dang it was unsucceful check the email and password", 'danger')
    return render_template('login.htm', title='Login', form = form)

@app.route('/pygalexample')
def pygalexample():
    graph = pygal.Line()
    graph.title = 'Browser usage evolution (in %)'
    graph.x_labels = map(str, range(2002, 2013))
    graph.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    graph.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    graph.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    graph.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    graph_data = graph.render_data_uri()
    return render_template("graphing.htm", graph_data=graph_data)
    """return graph.render_response()
    return render_template('graphing.htm')"""

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path =os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.htm', title='Account', image_file=image_file, form = form)

@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.htm', title='New Post', form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.htm', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been update', 'sucess')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.htm', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
   
@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('user_posts.htm', posts=posts, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, go to this link: 
    {url_for('reset_token', token = token,  _external = True)}'''
    mail.send(msg)

@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_request(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('A password reset e-mail had been send ', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.htm', title='Reset Password', form= form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired link', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=brcypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has now been updated', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.htm', title='Reset Password', form= form)


"""if __name__ == '__main__':
    app.run(debug=True)"""