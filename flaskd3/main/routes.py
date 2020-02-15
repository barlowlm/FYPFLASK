from flask import render_template, request, flash, Blueprint
from flaskd3.models import Post#, Commenting
from flask_login import login_user, current_user, logout_user, login_required
from flaskd3 import db
import time, datetime
from datetime import date, timedelta 
import datedelta

import os
import json
from werkzeug.utils import secure_filename
import pygal
import time


#print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(1438094031))
main = Blueprint('main', __name__)

from flaskd3 import dropzone

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
"""dropzone = Dropzone(app)"""
"""def create_app(config):
    app = Flask(__name__)
    dropzone.init_app(app)
    return app"""

@main.route('/stats')
@login_required
def stats():
    graph = pygal.Line()
    graph.title = 'Browser usage evolution (in %)'
    graph.x_labels = map(str, range(2002, 2013))
    graph.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    graph.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    graph.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    graph.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    graph_data = graph.render_data_uri()
    
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

    
    
    with open(os.path.join(APP_ROOT, 'data/comments.json')) as file2:
        data_comments = json.load(file2)

    with open(os.path.join(APP_ROOT, 'data/account_activity.json')) as file3:
        data_account_activity = json.load(file3)
    
    with open(os.path.join(APP_ROOT, 'data/friends.json')) as file4:
        data_friends = json.load(file4)

    '''    with open(os.path.join(APP_ROOT, 'data/your_address_books.json')) as file5:
            data_your_address_book = json.load(file5)'''

    '''    with open(os.path.join(APP_ROOT, 'data/your_address_books.json')) as file6:
            data_your_address_book = json.load(file6)'''

    '''with open(os.path.join(APP_ROOT, 'data/your_off_facebook_activity.json')) as file7:
        data_your_off_facebook_activity = json.load(file7)'''

    react_timestamps =[]
    react_dates = []
    
    with open(os.path.join(APP_ROOT, 'data/posts_and_comments.json')) as file8:
        data_posts_and_comments = json.load(file8)
        #print(data_posts_and_comments.get('reactions')[2].get('timestamp'))
        for i in data_posts_and_comments.get('reactions'):
            #print (i.get('timestamp'))

            #print(datetime.date.fromtimestamp(i.get('timestamp')).isoformat())
            react_timestamps.append(datetime.date.fromtimestamp(i.get('timestamp')))

        print(react_timestamps)
        minimuim = datetime.date(2020,2,10)
        counter = 0
        react_count_according_to_date = []
        for i in react_timestamps: 
            #print(i) 
            if i <= minimuim:
            #if i.year <= minimuim.year and i.day <= minimuim.month and i.day <= minimuim.day:
                counter = counter + 1 #add counter for reacts per day
                if i < minimuim and i == minimuim - datedelta.DAY:
                    react_count_according_to_date.append(counter)
                    counter = 0
                    react_dates.append(minimuim)
                    #i = minimuim
                    minimuim = i
                
                elif i < minimuim: 
                    day = minimuim - datedelta.DAY
                    react_dates.append(day)
                    minimuim = i
                    react_count_according_to_date.append(0)
            
    line_chart = pygal.Bar()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

    line_data = line_chart.render_data_uri()

    line_chart = pygal.Bar()
    line_chart.title = 'reacts per day'
    line_chart.x_labels = map(str, range(0, 4338))
    line_chart.add('comments', react_count_according_to_date)

    line_data = line_chart.render_data_uri()

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

#target = os.path.join(APP_ROOT, 'data/')
target = os.path.join(APP_ROOT, 'data/')
print(target)
@main.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    
    if not os.path.isdir(target):
       os.mkdir(target)

    if request.method == 'POST':
        f = request.files.get('file')
        try:
            f.save(os.path.join(target, f.filename))
        except Exception:
            print("FilesSavedIndividually")
            
        
            """time.sleep(15)
        if os.path.isdir(os.path.join(APP_ROOT, 'data/comments.json')):"""

        flash('Your graphs have now been created, Go to the charts page to see your info', 'success')


    return render_template('upload.htm')

@main.route('/about')
def about():
    #name = request.args.get("name", "World")
    #return "<h1>About Page!</h1>"#f'Hello, {escape(name)}!'
    return render_template('about.htm')