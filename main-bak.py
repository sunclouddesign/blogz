from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:56b0lrzKFCPAnqqW@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Post', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_body = db.Column(db.Text(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, post_title, post_body, owner):
        self.post_title = post_title
        self.post_body = post_body
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'register_user','index','blog_archive','get_post','get_user']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

def get_blog_posts():

    return Post.query.all()

def get_users():

    return User.query.all()

def get_posts_by_user(usern):

    owner = User.query.filter_by(username=usern).first()
    id = owner.id
    return Post.query.filter_by(owner_id=id).all()

@app.route('/blog')
def blog_archive():
    users = get_users()
    blogs = get_blog_posts()
    #for blog in blogs:
    #    authorid = blog.owner_id 
    #    author_name = User.query.filter_by(id=authorid).first().username
        
    return render_template('blog.html',title="My Blog",blogs=blogs,users=users)

@app.route('/newpost', methods=['GET','POST'])
def new_post():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['body']
        new_post = Post(post_title,post_content,owner)
        db.session.add(new_post)
        db.session.commit()

        #One way to render the page
        post_id = str(new_post.id)
        return redirect("/post?id=" + post_id)
        #Another option
        #return render_template('blog.html',title="My Blog",single_post=Post.query.filter_by(id=new_post.id).first())
    else:
        return render_template('newpost.html',title="My Blog")

@app.route("/user")
def get_user():

    usern = request.args.get("author")
    #usern = 'noona'
    owner = User.query.filter_by(username=usern).first()
    posts = get_posts_by_user(usern)
    return render_template('blog.html', title="User Blog", author=owner,posts=posts)
    #owner = User.query.filter_by(id=ownerid).first()
    #return render_template('blog.html',title="User Blog",user_posts=get_users())
    #return render_template('blog.html',title="User Blog",user_posts=Post.query.filter_by(owner_id=ownerid).all())
    #return render_template('blog.html',title="User Blog",single_user=User.query.filter_by(id=userid).first())

@app.route("/post")
def get_post():

    postid = request.args.get("id")
    return render_template('blog.html',title="My Blog",single_post=Post.query.filter_by(id=postid).first())

@app.route('/')
def index():
    
    return render_template('index.html', users = get_users(), title="Blogzzzzz")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()
