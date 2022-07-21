from flask_app import app
from flask import Flask, render_template, request, redirect, session, request, flash
from flask_app.models import shoe, user, comment, like
from flask_app.models.like import Like



@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        
        'shoe_id':id,
        'user_id': session["user_id"]
    }
    if not Like.validate_like(data):
        return redirect(f"/shoe/{request.form['shoe.id']}")
    Like.save(data)
    return redirect(f"/shoe/{request.form['shoe.id']}")