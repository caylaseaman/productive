from flask import Flask, render_template, request, redirect, url_for, session
from fake_data import dogs, days, get_dog_by_handle, get_posts_by_handle, get_post_by_id, add_post_url
from database import get_list, insert_post, delete_post, switch_button, get_switch, get_switch_list
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FileField
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
import pymysql
import mysql.connector
import flask

app = Flask(__name__, template_folder="templates", static_url_path='/static')

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b'dshfabmsdbmasdmfjglq'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

users = {
    "rose": generate_password_hash("rose"),
    "chucky": generate_password_hash("chucky ")

}

class User():
    def __init__(self, username):
        self.username = username
        
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @classmethod
    def get(cls,username):
        return User(username)


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    username = StringField('Username')
    name = StringField('Name')
    bio = TextAreaField('Bio')
    age = IntegerField('Age')
    avatar = FileField('Avatar')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
    
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignUpForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password_hash = generate_password_hash(form.password.data)
#         bio = form.bio.data
#         age = form.age.data
#         name = form.name.data
#         avatar = form.avatar.data

#         print(avatar)
#         print(avatar.filename)

#         blob_service_client = BlobServiceClient.from_connection_string(secrets.blob_connection_string)
#         blob_client = blob_service_client.get_blob_client(container=secrets.container_name, blob=avatar.filename)
#         blob_client.upload_blob(avatar)
#         # validate 
#         # * not existing username
#         # * username/password are valid (not empty strings)
        
#         create_user(username, name, bio, age, password_hash, avatar.filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        # login_user(user)
        username = form.username.data
        password = form.password.data

        if username in users and \
            check_password_hash(users.get(username), password):
            
            user = User(username)
            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('feed'))
    return flask.render_template('login.html', form=form)

@app.route('/')
@login_required
def feed():
    lists = get_list()
    switch = get_switch_list()
    print(switch)
    print(current_user.username)
   
    return render_template('feed.html', days=days, lists=lists, switch=switch)
    
@app.route('/dog/<string:handle>')
def dog(handle):
    dog = get_dog_by_handle(handle)
    return render_template('dog.html', dog=dog, posts=get_posts_by_handle(handle))

@app.route('/post/<string:handle>/<string:id>')
def post(handle, id):
    dog = get_dog_by_handle(handle)
    return render_template('post.html', dog=dog, post=get_post_by_id(id))

@app.route('/create', methods = ['POST'])
@login_required
def create():
    content = request.form['post-content']
   
    # put content in db
    insert_post(content)
    return redirect(url_for('feed'))

@app.route('/delete')
@login_required
def delete():
    task_id = request.args.get('task_id')
    delete_post(task_id)
    return redirect(url_for('feed'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/switch/<int:btn_id>')
@login_required
def switch(btn_id):
    print(btn_id)
    switch_button(btn_id)
    return get_switch(btn_id)

if __name__ == "__main__":
    get_list()
    app.run(debug=True)