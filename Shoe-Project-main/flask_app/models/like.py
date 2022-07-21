from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import comment
from flask_app.models import shoe


class Likecount:
    db_name = 'fassion_shoes'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.shoe_id = db_data['shoe_id']
        self.user_id = db_data['user_id']
        self.nick_name = db_data['nick_name']
        self.likes = db_data['count']
        
    @classmethod
    def likescount(cls,data):
        query = "select *, count(likes.id) as count from shoes left join likes on shoes.id = likes.shoe_id left join users on likes.user_id = users.id where shoes.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)



class Like:
    db_name = 'fassion_shoes'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.shoe_id = db_data['shoe_id']
        self.user_id = db_data['user_id']
        self.nick_name = db_data['nick_name']
        self.likes = []
        
        
        
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO likes (shoe_id,user_id) VALUES (%(shoe_id)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @staticmethod
    def validate_like(data):
        is_valid = True
        query = "SELECT id from likes WHERE user_id = %(user_id)s AND shoe_id = %(shoe_id)s;"
        results = connectToMySQL(Like.db_name).query_db(query,data)
        if len(results) >=1:
            is_valid = False
        return is_valid 


