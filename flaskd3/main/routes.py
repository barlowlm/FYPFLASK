from flask import render_template, request, flash, Blueprint
from flaskd3.models import Post, FileContent#, Commenting
from flask_login import login_user, current_user, logout_user, login_required
from flaskd3 import db
import time, datetime
from datetime import date, timedelta 
import datedelta
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, DATA

import os
import json
from werkzeug.utils import secure_filename
import pygal
import time


#print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(1438094031))
main = Blueprint('main', __name__)

from flaskd3 import dropzone

APP_ROOT = os.path.dirname(os.path.abspath('/Users/Mathieux/Desktop/FYP/Flask_D3/flaskd3'))
"""dropzone = Dropzone(app)"""
"""def create_app(config):
    app = Flask(__name__)
    dropzone.init_app(app)
    return app"""

@main.route('/stats')
@login_required
def stats():

    #return graph.render_response()

    pie_chart = pygal.Pie(inner_radius=.4)
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)


    #print(os.path.join(APP_ROOT, 'data/graphtest.png'))
    #pie = pie_chart.render_to_png(os.path.join(APP_ROOT, 'data/graphtest.png'))
    pie = pie_chart.render_data_uri()

    comment_timestamps =[]
    comment_dates = []    
    
    with open(os.path.join(APP_ROOT, 'data/comments.json')) as file2:
        data_comments = json.load(file2)

        for i in data_comments.get('comments'):
            comment_timestamps.append(datetime.date.fromtimestamp(i.get('timestamp')))

        #print(comment_timestamps)
        minimuim = comment_timestamps[0]
        counter = 0
        comment_count_according_to_date = []

        for a in comment_timestamps: 
            # first and last not being recorded
            if minimuim >= a + datetime.timedelta(days=+30):
                comment_dates.append(a.strftime("%m/%Y"))
                comment_count_according_to_date.append(counter)
                gap = a - minimuim
                gap = (gap.days * -1) -1
                #print('NaaaaaaaA', gap)
             #for gaps in range(gap):
                #comment_count_according_to_date.append(0)
                #counter = counter + 1
                minimuim = a    
                counter = 0
            counter = counter + 1
            #minimuim = a

    session_timestamps =[]
    session_dates = []

    with open(os.path.join(APP_ROOT, 'data/account_activity.json')) as file3:
        data_account_activity = json.load(file3)

        for i in data_account_activity.get('account_activity'):
            session_timestamps.append(datetime.date.fromtimestamp(i.get('timestamp')))

        #print(session_timestamps)
        minimuim = session_timestamps[0]
        counter = 0
        session_count_according_to_date = []
        session_dates=[]

        for a in session_timestamps: 
            # first and last not being recorded
            if minimuim >= a + datetime.timedelta(days=+30):
                session_dates.append(a.strftime("%m/%Y"))
                session_count_according_to_date.append(counter)
                gap = a - minimuim
                gap = (gap.days * -1) -1
                #print('NaaaaaaaA', gap)
             #for gaps in range(gap):
                    #session_count_according_to_date.append(0)
                    #counter = counter + 1
                minimuim = a    
                counter = 0
            counter = counter + 1
            #minimuim = a

    friends=[]
    with open(os.path.join(APP_ROOT, 'data/friends.json')) as file4:
        data_friends = json.load(file4)

        for i in data_friends.get('friends'):
            friends.append(i.get('name'))

        print(friends)

    '''    with open(os.path.join(APP_ROOT, 'data/your_address_books.json')) as file5:
            data_your_address_book = json.load(file5)'''

    your_posts_1_timestamps =[]
    your_posts_1_dates = []
    with open(os.path.join(APP_ROOT, 'data/your_posts_1.json')) as file6:
        data_your_posts_1 = json.load(file6)

        for i in data_your_posts_1:#.get('reactions')"""
            your_posts_1_timestamps.append(datetime.date.fromtimestamp(i.get('timestamp')))
            

        minimuim = your_posts_1_timestamps[0]
        counter = 0
        your_posts_1_count_according_to_date = []
        
        for a in your_posts_1_timestamps: 
        # first and last not being recorded
            if minimuim >= a + datetime.timedelta(days=+30):
                your_posts_1_dates.append(a.strftime("%m/%Y"))
                your_posts_1_count_according_to_date.append(counter)
                gap = a - minimuim
                gap = (gap.days * -1) -1
                #print('NaaaaaaaA', gap)
             #for gaps in range(gap):
                    #your_posts_1_count_according_to_date.append(0)
                    #counter = counter + 1
                minimuim = a    
                counter = 0
            counter = counter + 1
            #minimuim = a


    '''with open(os.path.join(APP_ROOT, 'data/your_off_facebook_activity.json')) as file7:
        data_your_off_facebook_activity = json.load(file7)'''

    react_timestamps =[]
    react_dates = []
    with open(os.path.join(APP_ROOT, 'data/posts_and_comments.json')) as file8:
        data_posts_and_comments = json.load(file8)

        for i in data_posts_and_comments.get('reactions'):
            react_timestamps.append(datetime.date.fromtimestamp(i.get('timestamp')))

        #print(react_timestamps)
        minimuim = react_timestamps[0]
        counter = 0
        react_count_according_to_date = []
        
        for a in react_timestamps: 
        # first and last not being recorded
            if minimuim >= a + datetime.timedelta(days=+30):
                react_dates.append(a.strftime("%m/%Y"))
                react_count_according_to_date.append(counter)
                gap = a - minimuim
                gap = (gap.days * -1) -1
                #print('NaaaaaaaA', gap)
             #for gaps in range(gap):
                    #react_count_according_to_date.append(0)
                    ##counter = counter + 1
                minimuim = a    
                counter = 0
            counter = counter + 1
            #minimuim = a


    line_chart = pygal.Bar()
    line_chart.title = 'Browser usage evolution (in %)'
           
    line_data = line_chart.render_data_uri()
    line_chart = pygal.Bar()
    line_chart.title = 'reacts per day'
    line_chart.x_labels = map(str, list(reversed(react_dates)))
    line_chart.add('Reacts', list(reversed(react_count_according_to_date)))
    line_chart.add('Commets', list(reversed(comment_count_according_to_date)))
    line_chart.add('Sessions', list(reversed(session_count_according_to_date)))
    line_chart.add('Posts', list(reversed(your_posts_1_count_according_to_date)))

    line_data = line_chart.render_data_uri()

    graph = pygal.Line()
    graph.title = 'Browser usage evolution (in %)'
    graph.x_labels = map(str, react_dates)
    graph.add('reacts', react_count_according_to_date)
    graph.add('sessions', session_count_according_to_date)
    graph.add('Comments', comment_count_according_to_date)
    graph.add('Posts', your_posts_1_count_according_to_date)

    graph_data = graph.render_data_uri()
        
    #print(react_timestamps)
    #print(react_dates)
    #print(react_count_according_to_date)
    
    return render_template("stats.htm", graph_data=graph_data, line_data=line_data, pie=pie)

    """for comment in data['comments']:
            print(comment)
            print('\n')
        
        longcomments1 = Commenting(**data)
        db.session.add(longcomments1)
        db.session.commit()
        print(Commenting.query.all())"""
    
    """return render_template('stats.htm')"""
   
@main.route('/', methods=["GET","POST"])
@main.route('/home', methods=["GET","POST"])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.htm', posts=posts)

target1 = os.getcwd() + '/data/'
print(target1)
target = os.path.join(APP_ROOT, 'data/')
print(target)

files = UploadSet('files', DATA)
#app.config['UPLOADED_PHOTO_DEST'] = 'static/data'
#configure_uploads(app, files)

@main.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    
    if not os.path.isdir(target1):
       os.makedirs(target1,exist_ok=True)

    if request.method == 'POST':
        f = request.files.get('file')
        try:
            f.save(os.path.join(target1, f.filename))
            #f.save('static/data/' + request.files['file'])
            #filedb = FileContent(name = f.filename, data=f.read())
            #print(filedb.filename)
            #db.session.add(filedb)
            #db.session.commit()
        except Exception:
            print("FilesSavedIndividually")
   
            """time.sleep(15)
        if os.path.isdir(os.path.join(APP_ROOT, 'data/comments.json')):"""

        flash('Your graphs have now been created, Go to the charts page to see your info', 'success')

    return render_template('upload.htm')

@main.route('/download')
def download():
    file_data = FileContent.query.first()
    return send_file(BytesIO(file_data.data), attachment_filename='flask.pdf', as_attachment=True)

@main.route('/about')
def about():
    #name = request.args.get("name", "World")
    #return "<h1>About Page!</h1>"#f'Hello, {escape(name)}!'


    return render_template('about.htm')