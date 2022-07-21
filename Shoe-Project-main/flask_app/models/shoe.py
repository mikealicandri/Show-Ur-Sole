from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import comment
from flask_app.models import like

class Shoe:
    db_name = 'fassion_shoes'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.brand = db_data['brand']
        self.model = db_data['model']
        self.size = db_data['size']
        self.price = db_data['price']
        self.description = db_data['description']
        # self.photo = db_data['photo']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.nick_name = db_data['nick_name']
        self.likes = db_data['count']
        


    @classmethod 
    def save(cls,data):
        query = 'INSERT INTO shoes (name, brand, model, size, price, description,user_id) VALUES(%(name)s,%(brand)s,%(model)s,%(size)s,%(price)s,%(description)s,%(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shoes;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_shoes = []
        for row in results:
            all_shoes.append( cls(row) )
        return all_shoes
            
    
    @classmethod
    def get_all_with_extra(cls):
        query = "SELECT *,count(likes.id) as count FROM shoes left join users on user_id = users.id left join likes on shoes.id = likes.shoe_id group by shoes.id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_shoes = []
        for row in results:
            all_shoes.append( cls(row) )
        return all_shoes
    
    # @classmethod
    # def get_all_with_creator(cls):
    #     query = "SELECT * FROM shoes left join users on user_id = users.id;"
    #     results =  connectToMySQL(cls.db_name).query_db(query)
    #     all_shoes = []
    #     for row in results:
    #         all_shoes.append( cls(row) )
    #     return all_shoes
    
    
    @classmethod
    def delete_like(cls, data):
        query = "DELETE FROM likes Where shoe_id = %(id)s;"       
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments Where shoe_id = %(id)s;"  
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shoes Where id = %(id)s;"
        
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_one_with_extra(cls,data):
        query = "SELECT *,count(likes.id) as count FROM shoes left join users on user_id = users.id left join likes on shoes.id = likes.shoe_id WHERE shoes.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )
    
    
    # @classmethod
    # def get_one(cls,data):
    #     query = "SELECT * FROM shoes left join users on user_id = users.id WHERE shoes.id = %(id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query,data)
    #     return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE shoes SET name=%(name)s, brand=%(brand)s, model=%(model)s, size=%(size)s, price=%(price)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM shoes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    # what is sneaker head??
    @classmethod
    def get_all_shoes_with_sneaker_head(cls):
        query = "SELECT * FROM shoes JOIN users ON shoes.user_id = users.id;"
        results = connectToMySQL('fassion_shoes').query_db(query)
        all_shoes = []
        for row in results:
            one_shoe = cls(row)
            one_shoes_sneaker_head_info = {
            "id": row['id'],
            "first_name": row['first_name'],
            "last_name": row['last_name'],  
            "email": row['email'],
            "password": row['password'],
            "created_at": row['created_at'],
            "updated_at": row['updated_at']
            }
            sneaker_head = user.User(one_shoes_sneaker_head_info)
            one_shoe.sneaker_head = sneaker_head
            all_shoes.append(one_shoe)
        return all_shoes

    @staticmethod
    def validate_shoe(shoe):
        is_valid = True
        if len(shoe['name']) < 3:
            is_valid = False
            flash('Name requires at least 4 characters','shoe')
        if len(shoe['brand']) < 1:
            is_valid = False
            flash('Brand requres 2 characters','shoe')
        if len(shoe['model']) < 3:
            is_valid = False
            flash('Model required 3 characters','shoe')
        return is_valid
    