from flask import render_template,url_for,flash,redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog.models import User,Post

posts=[
    {
        'author':'Hari',
        'title':'Blog post 1',
        'content':'First post content',
        'date_posted':'July 7,2019'        
        },
    {
        'author':'Jeevanth',
        'title':'Blog post 2',
        'content':'Second post content',
        'date_posted':'July 7,2019'        
        },
    {
        'author':'Manissh',
        'title':'Blog post 3',
        'content':'Third post content',
        'date_posted':'July 7,2019'        
        }
    ]

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',posts=posts,title='Home')

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data }...!','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form,title='Register')

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data=='dheva1999@gmail.com' and form.password.data=='password':
            flash(f'Log in successful..!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful..!','danger')
    
    return render_template('login.html',form=form,title='Login')

@app.route('/about')
def about():
    return render_template('about.html',title='About')
