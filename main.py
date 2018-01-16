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
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User/password incorrect or user does not exist', 'error')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        Email_error = ''
        Password_error = ''
        Verify_error = ''
        

        if len(email) < 3 or len(email) > 20 or " " in email or email == "":
            Email_error = "Your entry must be between 3 and 20 characters and contain no spaces. Required field."
        if len(password) < 3 or len(password) > 20 or " " in password or password == "":
            Password_error = "Your entry must be between 3 and 20 characters and contain no spaces. Required field."
        if len(verify) < 3 or len(verify) > 20 or " " in verify or verify == "":
            Verify_error = "Your entry must be between 3 and 20 characters and contain no spaces. Required field."
            
        if email:
            if "." not in email and "@" not in email:
                Email_error = "Please check and re-submit. Please do not use spaces."

        if password != verify:
            Password_error = "Password and Verify Password fields must match."
            Verify_error = "Password and Verify Password fields must match."

        if not Email_error and not Password_error and not Verify_error:
            email = request.form['email']
            return render_template('blogs.html', email=email)
            
        else:
            return render_template('register.html', email=email, Email_error=Email_error, password='',Password_error=Password_error, verify='', Verify_error=Verify_error)


        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return "<h1>User already exists.</h1>"

    return render_template('register.html')


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    
    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name, owner)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(completed=False,owner=owner).all()
    completed_blogs = blog.query.filter_by(completed=True,owner=owner).all()
    return render_template('blogs.html',title="My Blogs", 
        blogs=blogs, completed_blogs=completed_blogs)


@app.route('/finished-blog', methods=['POST'])
def finished_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    blog.completed = True
    db.session.add(blog)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()