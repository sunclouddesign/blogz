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

    posts = Post.query.all()
    return render_template('newpost.html')    

@app.route("/post")
def get_post():

    postid = request.args.get("id")
    #print(post_id)
    #post_id = Post.query.get(id)
    #postid = Post.query.get(id)
    #post = Post.query.filter_by(id=post_id).first()
    return render_template('blog.html',single_post=Post.query.filter_by(id=postid).first())
    #return redirect("/newpost?id=" + post_id)

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_name = request.form['title']
        post_content = request.form['body']
        new_post = Post(post_title=post_name,post_body=post_content)
        db.session.add(new_post)
        db.session.commit()
    
    #if request.method == 'GET' and 
    #posts = Post.query.all()
    #completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('blog.html', posts = get_blog_posts(), title="My Blog")
    #return render_template('ratings.html', movies = get_watched_movies())

#@app.route('/delete-task', methods=['POST'])
#def delete_task():
#
#    task_id = int(request.form['task-id'])
#    task = Task.query.get(task_id)
#    task.completed = True
#    db.session.add(task)
#    db.session.commit()

#    return redirect('/')


if __name__ == '__main__':
    app.run()
