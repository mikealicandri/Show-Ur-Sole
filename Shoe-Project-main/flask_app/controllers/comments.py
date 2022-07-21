from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.shoe import Shoe
from flask_app.models.comment import Comment

@app.route('/comment', methods=['POST'])
def postcomment():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "comment":request.form['comment'],
        "shoe_id":request.form['shoe.id'],
        "user_id":session['user_id']
    }
    Comment.save(data)
    return redirect(f"/shoe/{request.form['shoe.id']}")



