from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskd3 import db
from flaskd3.models import Post
from flaskd3.posts.forms import PostForm
from flaskd3.users.utils import save_picture
from flaskd3.main.routes import pygal
import PIL
import pysvg #import structures
import cairo
#import pysvg.builders
#import pysvg.text
#import subprocess
posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    line_data = pygal.Bar()
    line_data = line_data.render_to_png('flaskd3/static/graph_pics/default.png')
    form = PostForm()
    post = Post()
    if form.validate_on_submit():
        if form.image_file.data:
            graph_file = save_picture('graph_pics', form.image_file.data)  
            post.image_file = graph_file
        post.title = form.title.data 
        post.content = form.content.data 
        post.author = current_user
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
    else:
        post.image_file = 'default.jpg'
    image_file = url_for('static', filename='graph_pics/' + post.image_file)
    return render_template('create_post.htm', image_file=image_file, title='New Post', form=form, legend='New Post')





@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.htm', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.htm', title='Update Post', form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))