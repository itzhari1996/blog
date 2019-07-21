import os
from PIL import Image
from flask import render_template,url_for,flash,redirect,request
from flaskblog import app,db,bcrypt
from flaskblog.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
from flaskblog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
from secrets import token_hex

'''posts=[
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
    ]'''

@app.route('/home')
@login_required
def home():
    posts=Post.query.all()
    return render_template('index.html',posts=posts,title='Home')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1=User(username=form.username.data,password=hashed_pwd,email=form.email.data)
        db.session.add(user1)
        db.session.commit()
        flash(f'Account created for {form.username.data }...!','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form,title='Register')

@app.route('/login',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            nextpage=request.args.get('next')
            flash(f'Log in successful..!','success')
            return redirect(nextpage) if nextpage else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful..!','danger')

    return render_template('login.html',form=form,title='Login')

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    pichash=token_hex(8)
    _,picext=os.path.splitext(form_picture.filename)
    picname=pichash+picext
    picpath=os.path.join(app.root_path,'static/images',picname)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picpath)
    return picname

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        print(form.picture.data)
        if form.picture.data:
            profile_pic=save_picture(form.picture.data)
            print(profile_pic)
            current_user.image_file=profile_pic
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Details updated successfully','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='images/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post1=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post1)
        db.session.commit()
        flash('Your Post has been created Successfully!...','success')
        return redirect(url_for('home'))
    return render_template('new_post.html',title='New Post',form=form)

@app.route('/post/<int:post_id>')
@login_required
def edit_post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)