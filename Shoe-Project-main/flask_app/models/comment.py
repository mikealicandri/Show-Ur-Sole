from flask_app.config.mysqlconnection import connectToMySQL
import re	 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import shoe, user


class Comment:
    db_name = "fassion_shoes"
    def __init__(self,data):
        self.id = data['id']
        self.nick_name = data['nick_name']
        self.shoe_id = data['shoe_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comment = data['comment']
        
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO comments (comment, shoe_id, user_id) VALUES(%(comment)s,%(shoe_id)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)  
    
    @classmethod    
    def get_comment_with_nick_name(cls,data):  
        query = "Select * from comments left join users on user_id = users.id where shoe_id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
        
        