from flask import render_template, request, flash, Blueprint, redirect
from flaskd3.models import Post, FileContent#, Commenting
from flask_login import login_user, current_user, logout_user, login_required
from flaskd3 import db, dropzone
from flaskd3.main.forms import SubmitGraphForm
from flaskd3.users.utils import save_picture
from flask import url_for
import cairosvg
import time, datetime
from datetime import date, timedelta 
import datedelta
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, DATA
from flaskd3 import models
import os
import json
from werkzeug.utils import secure_filename
import pygal
import time
from collections import Counter

import re 
import string

#print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(1438094031))
main = Blueprint('main', __name__)


APP_ROOT = os.path.dirname(os.path.abspath('/Users/Mathieux/Desktop/FYP/Flask_D3/flaskd3'))

@main.route('/stats', methods=['GET','POST'])
@login_required
def stats():
   
    comment_timestamps = []
    comment_dates = []     
    with open(os.path.join(APP_ROOT, 'data/comments.json')) as file2:
        data_comments = json.load(file2)

        for i in data_comments.get('comments'):
            comment_timestamps.append(datetime.date.fromtimestamp(i.get('timestamp')))

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
                minimuim = a    
                counter = 0
            counter = counter + 1

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
                minimuim = a    
                counter = 0
            counter = counter + 1

   #friends=[]
    #with open(os.path.join(APP_ROOT, 'data/friends.json')) as file4:
    #    data_friends = json.load(file4)

    #    for i in data_friends.get('friends'):
    #        friends.append(i.get('name'))"""

    '''    with open(os.path.join(APP_ROOT, 'data/your_address_books.json')) as file5:
            data_your_address_book = json.load(file5)'''

    your_posts_1_timestamps =[]
    your_posts_1_dates = []
    with open(os.path.join(APP_ROOT, 'data/your_posts_1.json')) as file6:
        data_your_posts_1 = json.load(file6)
        for i in data_your_posts_1:
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
                minimuim = a    
                counter = 0
            counter = counter + 1

    '''with open(os.path.join(APP_ROOT, 'data/your_off_facebook_activity.json')) as file7:
        data_your_off_facebook_activity = json.load(file7)'''

    react_timestamps =[]
    react_friends = []
    react_dates = []
    titles=[]
    sentence=[]
    dict_timestamp_friend={}

    with open(os.path.join(APP_ROOT, 'data/posts_and_comments.json')) as file8:
        data_posts_and_comments = json.load(file8)
        prev =''
        names1 = []
        user = data_posts_and_comments.get('reactions')[0].get('data')[0].get('reaction').get('actor')
        usersplit = user.split()
        #print(usersplit)
        #print("hiiiiiiiiiiiiiiiiiiiii"+ usersplit)

        for i in data_posts_and_comments.get('reactions'):
            react_timestamps.append(datetime.date.fromtimestamp(i.get('timestamp')))
            res = re.sub('['+string.punctuation+']', '' , i.get('title')).split()
            titles.append(res)
            #print(datetime.date.fromtimestamp(i.get('timestamp')))
            count = 0
            for a in res:
                if (a not in usersplit and a != 'Ladias' and a != 'likes'
                and a != 'liked' and a != 'his' and a != 'her' and a != 'own' and a != 'photo' 
                and a != 'comment' and a != 'post' and a != 'video' and a != 'a' 
                and a != 'on' and a != 'timeline'and a != 'album' and a != 'in' and count <= 1
                and a != 'reacted' and a != 'to'):
                    if count == 1:
                        names1.append(str(prev +' '+ a))
                        temp = str(datetime.date.fromtimestamp(i.get('timestamp')))
                        dict_timestamp_friend.update({temp: str(prev +' '+ a)})
                        #print(str(prev +' '+ a))
                    prev = a
                    count = count+1

        #print(dict_timestamp_friend)

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
                minimuim = a    
                counter = 0
            counter = counter + 1



    addapted_friendlist=[]
    addapted_reacts=[]
    listtimestamp =[]
    if request.method == 'POST' and "slider" in request.form:
        react_dates = []
        dict_timestamp_friend =[]
        listnames =[]
        with open(os.path.join(APP_ROOT, 'data/posts_and_comments.json')) as file9:
            data_posts_and_comments = json.load(file9)
            prev =''
            names1 = []
            user = data_posts_and_comments.get('reactions')[0].get('data')[0].get('reaction').get('actor')
            usersplit = user.split()
            print(usersplit)
            #print("hiiiiiiiiiiiiiiiiiiiii"+ usersplit)

            for i in data_posts_and_comments.get('reactions'):
                react_timestamps.append(datetime.date.fromtimestamp(i.get('timestamp')))
                temp = datetime.date.fromtimestamp(i.get('timestamp'))
                res = re.sub('['+string.punctuation+']', '' , i.get('title')).split()
                titles.append(res)
                #print(datetime.date.fromtimestamp(i.get('timestamp')))
                count = 0
                for a in res:
                    if (a not in usersplit and a != 'Ladias' and a != 'likes'
                    and a != 'liked' and a != 'his' and a != 'her' and a != 'own' and a != 'photo' 
                    and a != 'comment' and a != 'post' and a != 'video' and a != 'a' 
                    and a != 'on' and a != 'timeline'and a != 'album' and a != 'in' and count <= 1
                    and a != 'reacted' and a != 'to'):
                        if count == 1:
                            names1.append(str(prev +' '+ a))
                            #temp = str(datetime.date.fromtimestamp(i.get('timestamp')))
                            temp = datetime.date.fromtimestamp(i.get('timestamp'))
                            #dict_timestamp_friend.update({str(prev +' '+ a): temp})
                            dict_timestamp_friend.append([str(prev +' '+ a), temp])
                            listnames.append(str(prev +' '+ a))
                            listtimestamp.append(temp)
                            #print(str(prev +' '+ a) + " "+ temp)
                        prev = a
                        count = count+1

            listtimefriend=[listnames,listtimestamp]
            print(listnames)
            print(len(listtimestamp))
            friendCountFromSlider = request.form['slider']
            print("slider  " + friendCountFromSlider)
            counter = Counter(listnames)
            most_occur = counter.most_common(int(friendCountFromSlider))

            print("aaaaaaaaaaah")

            most_occured_names = []
            for i in most_occur:
                most_occured_names.append(i[0])
            print(most_occured_names)
            
            #listnames_output = listnames.copy() 
            #listtimefriend_output = listtimefriend.copy()
            listnames_output = []
            listtimestamp_output = []
            print(listtimefriend)
            for elem, elem1 in zip(listnames,listtimestamp):
                print(elem)
                if elem in most_occured_names:
                    listnames_output.append(elem)
                    listtimestamp_output.append(elem1)
            
            print(listnames_output)
            print(listtimestamp_output)
            minimuim = react_timestamps[0]
            counter = 0
            react_count_according_to_date = []

            for a in listtimestamp_output: 
            # first and last not being recorded
                if minimuim >= a + datetime.timedelta(days=+30):
                    react_dates.append(a.strftime("%m/%Y"))
                    react_count_according_to_date.append(counter)
                    gap = a - minimuim
                    gap = (gap.days * -1) -1
                    minimuim = a    
                    counter = 0
                counter = counter + 1
                
 ####           

    line_chart = pygal.Bar()
    line_chart.title = 'Line Graph'
    line_data = line_chart.render_data_uri()
    line_chart = pygal.Bar()
    line_chart.title = 'reacts per day'
    line_chart.x_labels = map(str, react_dates)
    line_chart.add('Reacts', react_count_according_to_date)
    line_chart.add('Commets', comment_count_according_to_date)
    line_chart.add('Posts', your_posts_1_count_according_to_date)
    line_data = line_chart.render_data_uri()
    linepng = line_chart.render_to_png('flaskd3/static/graph_pics/line.png')

    line_chart1 = pygal.Bar()
    line_chart1.title = 'Line Graph1'
    line_chart1 = pygal.Bar()
    line_chart1.title = 'session'
    line_chart1.add('Sessions', list(reversed(session_count_according_to_date)))
    line_data1 = line_chart1.render_data_uri()
    linepng1 = line_chart1.render_to_png('flaskd3/static/graph_pics/linesession.png')

    graph = pygal.Line()
    graph.title = 'Bar Chart'
    graph.x_labels = map(str, react_dates)
    graph.add('reacts', react_count_according_to_date)
    graph.add('sessions', session_count_according_to_date)
    graph.add('Comments', comment_count_according_to_date)
    graph.add('Posts', your_posts_1_count_according_to_date)
    graph_data = graph.render_data_uri()
    graphpng = graph.render_to_png('flaskd3/static/graph_pics/graph.png')

    graph1 = pygal.Line()
    graph1.title = 'Bar Chart'
    graph1.x_labels = map(str, react_dates)
    graph1.add('sessions', session_count_according_to_date)
    graph_data1 = graph1.render_data_uri()
    graphpng1 = graph1.render_to_png('flaskd3/static/graph_pics/graph1.png')

    pie_chart = pygal.Pie(inner_radius=.4)
    pie_chart.title = 'Pie chart'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    pie = pie_chart.render_data_uri()
    piepng = pie_chart.render_to_png('flaskd3/static/graph_pics/pie.png')
   
    Averag_reacts_per_months = sum(react_count_according_to_date)/(len(react_count_according_to_date)+1)
    Averag_comments_per_months = sum(comment_count_according_to_date)/len(comment_count_according_to_date)
    Averag_sessions_per_months = sum(session_count_according_to_date)/len(session_count_according_to_date)
    Averag_posts_per_months = sum(your_posts_1_count_according_to_date)/len(your_posts_1_count_according_to_date)   
       

    postpie = Post()
    if request.method == 'POST' and "postpie" in request.form:
        print("pie")
        piepng = pie_chart.render_to_png('flaskd3/static/graph_pics/pie.png')# replace pie.png with variable filename: next line also
        postpie.image_file = 'pie.png'
        print(postpie.image_file)
        #postpie.image_file = pie_chart.render_data_uri()
        postpie.title = current_user.username + " stats:"
        postpie.content = ("My average reactions per month are: "+ str(Averag_reacts_per_months) 
        + "\nMy average comments per month are: " + str(Averag_comments_per_months) 
        + "\nMy average sessions per month are: " +str(Averag_sessions_per_months) 
        + "\nMy average posts per month are: " +str(Averag_posts_per_months))
        postpie.author = current_user
        db.session.add(postpie)
        db.session.commit()
        flash('Your postpie has been created', 'success')
        #graph_file = save_picture('graph_pics', piepng)
        return render_template("stats.htm", graph_data=graph_data, line_data=line_data, line_data1=line_data1, graph_data1=graph_data1, pie=pie, 
        Averag_reacts_per_months=Averag_reacts_per_months, Averag_comments_per_months=Averag_comments_per_months,
        Averag_post_per_months = Averag_posts_per_months)
   
    postbar = Post()
    if request.method == 'POST' and "postbar" in request.form:
        print("bar")
        barpng = graph.render_to_png('flaskd3/static/graph_pics/bar.png')# replace pie.png with variable filename: next line also
        postbar.image_file = 'linechart.png'
        #postbar.image_file = pie_chart.render_data_uri()
        postbar.title = current_user.username + " stats:"
        postbar.content = ("My average reactions per month are: "+ str(Averag_reacts_per_months) 
        + "\nMy average comments per month are: " + str(Averag_comments_per_months) 
        + "\nMy average sessions per month are :" +str(Averag_sessions_per_months) 
        + "\nMy average posts per month are: " +str(Averag_posts_per_months))
        postbar.author = current_user
        db.session.add(postbar)
        db.session.commit()
        flash('Your postbar has been created', 'success')
        #graph_file = save_picture('graph_pics', piepng)
        return render_template("stats.htm", graph_data=graph_data, line_data=line_data, pie=pie,line_data1=line_data1,
         Averag_reacts_per_months=Averag_reacts_per_months, Averag_comments_per_months=Averag_comments_per_months,
          Averag_post_per_months = Averag_posts_per_months, graph_data1=graph_data1)
    
    postline = Post()
    if request.method == 'POST' and "postline" in request.form:
        print("line")
        linepng = line_chart.render_to_png('flaskd3/static/graph_pics/line.png')# replace pie.png with variable filename: next line also
        postline.image_file = 'graph.png'
        print(postline.image_file)
        #postline.image_file = pie_chart.render_data_uri()
        postline.title = current_user.username + "stats:"
        postline.content = ("My average reactions per month are: "+ str(Averag_reacts_per_months) 
        + " \nMy average comments per month are: " + str(Averag_comments_per_months) 
        + " \nMy average sessions per month are: " +str(Averag_sessions_per_months) 
        + "\nMy average posts per month are: " +str(Averag_posts_per_months))
        postline.author = current_user
        db.session.add(postline)
        db.session.commit()
        flash('Your post has been created', 'success')
        #graph_file = save_picture('graph_pics', piepng)
        image_file = url_for('static', filename='graph_pics/' + postline.image_file)
        return render_template("stats.htm", graph_data=graph_data, line_data=line_data,line_data1=line_data1,
         pie=pie, Averag_reacts_per_months=Averag_reacts_per_months, Averag_comments_per_months=Averag_comments_per_months,
        Averag_post_per_months = Averag_posts_per_months, graph_data1=graph_data1)

    graphForm = SubmitGraphForm()
    graphForm.image_file.data = line_chart.render_to_png('flaskd3/static/graph_pics/linechart.png')
    
    
    """if graphForm.validate_on_submit():
        print("hello")
        graph_file = save_picture('graph_pics', graphForm.image_file.data)
        
        return redirect((url_for('/home')))
    else:
        post.image_file = 'default.jpg'"""
       
    
    """image_file_bar = url_for('static', filename='graph_pics/' + postbar.image_file)
    image_file_pie = url_for('static', filename='graph_pics/' + postpie.image_file)
    image_file_line = url_for('static', filename='graph_pics/' + postline.image_file)
    print(postbar.image_file)
    print(postline.image_file)
    print(postpie.image_file) """
        
    #post = Post(title =  , content = form.content.data,  author = current_user, image_file = line_data )# continue from here 
    return render_template("stats.htm", graph_data=graph_data, line_data=line_data, line_data1=line_data1,
     pie=pie, Averag_reacts_per_months=Averag_reacts_per_months, Averag_comments_per_months=Averag_comments_per_months,
        Averag_post_per_months = Averag_posts_per_months, Averag_sessions_per_months= Averag_sessions_per_months, graph_data1=graph_data1)
  
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
        except Exception:
            print("FilesSavedIndividually")
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
