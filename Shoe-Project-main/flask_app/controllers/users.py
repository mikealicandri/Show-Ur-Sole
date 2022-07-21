from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.shoe import Shoe
from flask_app.models.comment import Comment
from flask_app.models.like import Like
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_and_registration')
def login_page():
    return render_template('login_and_registration.html')

@app.route('/new_user',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/login_and_registration')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "nick_name": request.form['nick_name'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/login_and_registration')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login_and_registration')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/user/created')
def show_names():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    return render_template('dashboard.html',users=User.get_all_users(user_data))
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

