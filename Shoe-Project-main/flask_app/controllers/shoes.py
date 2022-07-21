from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.shoe import Shoe
from flask_app.models.comment import Comment
from flask_app.models.like import Like, Likecount

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('dashboard.html',shoes=Shoe.get_all_with_extra(), user=User.get_by_id(data))

@app.route('/new/shoe')
def new_shoe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('add_shoe.html',user=User.get_by_id(data))

@app.route('/create/shoe', methods=['POST'])
def create_shoe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Shoe.validate_shoe(request.form):
        return redirect('/new/shoe')
    data = {
        'name': request.form['name'],
        'brand': request.form['brand'],
        'model': request.form['model'],
        'size': request.form['size'],
        'price': request.form['price'],
        'description': request.form['description'],
        'photo': request.form['photo'],
        'user_id': session['user_id']
    }
    Shoe.save(data)
    return redirect ('/dashboard')

@app.route('/edit/shoe/<int:id>')
def edit_shoe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_shoe.html",shoe=Shoe.get_one_with_extra(data),user=User.get_by_id(user_data))

@app.route('/update/shoe/<int:id>',methods=['POST'])
def update_shoe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Shoe.validate_shoe(request.form):
        return redirect('/dashboard')
    data = {
        'id':id,
        'name': request.form['name'],
        'brand': request.form['brand'],
        'model': request.form['model'],
        'size': request.form['size'],
        'price': request.form['price'],
        'description': request.form['description'],
        'user_id': session['user_id']       
    }
    Shoe.update(data)
    return redirect('/dashboard')

@app.route('/shoe/<int:id>')
def show_shoe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("shoe.html",shoe=Shoe.get_one_with_extra(data),user=User.get_by_id(user_data), comments=Comment.get_comment_with_nick_name(data))


@app.route('/delete/shoe/<int:id>')
def destroy_shoe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Shoe.delete_comment(data)
    Shoe.delete_like(data)
    Shoe.delete(data)
    return redirect('/dashboard')



