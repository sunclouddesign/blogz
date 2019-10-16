from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:56b0lrzKFCPAnqqW@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_body = db.Column(db.Text(500))

    def __init__(self, post_title, post_body):
        self.post_title = post_title
        self.post_body = post_body

def get_blog_posts():

    return Post.query.all()

@app.route('/blog')
def blog_archive():
    
    return render_template('blog.html',posts=get_blog_posts(),title="My Blog")

@app.route('/newpost', methods=['GET','POST'])
def new_post():

    if request.method == 'POST':
        post_name = request.form['title']
        post_content = request.form['body']
        new_post = Post(post_title=post_name,post_body=post_content)
        db.session.add(new_post)
        db.session.commit()

        #One way to render the page
        post_id = str(new_post.id)
        return redirect("/post?id=" + post_id)
        #Another option
        #return render_template('blog.html',title="My Blog",single_post=Post.query.filter_by(id=new_post.id).first())
    else:
        return render_template('newpost.html',title="My Blog")


@app.route("/post")
def get_post():

    postid = request.args.get("id")
    return render_template('blog.html',title="My Blog",single_post=Post.query.filter_by(id=postid).first())

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_name = request.form['title']
        post_content = request.form['body']
        new_post = Post(post_title=post_name,post_body=post_content)
        db.session.add(new_post)
        db.session.commit()
    
    return render_template('blog.html', posts = get_blog_posts(), title="My Blog")


if __name__ == '__main__':
    app.run()
