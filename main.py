from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '7h1sh@sb33n7h3h@rd3s7p@r7'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    name = ""
    body = ""
    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']
        error = False
        if not name:
            flash("Blog must have a Title!", 'error')
            error = True
        if not body:
            flash("Blog must have a Body!", 'error')
            error = True
        if not error:
            blog = Blog(name,body)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blogs?id={0}'.format(blog.id))
    blogs = Blog.query.all()
    return render_template('newpost.html',title="New Post", 
        blogs=blogs)


@app.route('/blogs')
def all_blogs():
    blogid = request.args.get('id')
    if blogid:
        blogid = int(blogid)
        blogs = Blog.query.get(blogid)
        return render_template('ind_post.html', blogs=blogs)         
    blogs = Blog.query.all()
    return render_template('blogs.html', title="My Blogs", blogs=blogs)


if __name__ == '__main__':
    app.run()