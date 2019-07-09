from flask import Flask
from flask import render_template,url_for,flash,redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SECRET_KEY']='0cb6037aea1c9e3b6d2f67c0b59c7985'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(150), unique=True, nullable=False)
    image_file=db.Column(db.String(20),default='default.jpg', nullable=False)
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f"user('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), unique=True, nullable=False)
    dateposted=db.Column(db.DateTime, nullable=False, default=datetime.now)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"user('{self.title}','{self.dateposted}')"

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

if __name__=='__main__':
    app.run(debug=True)