from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA=Z]+$')

from flask import flash
from flask_app import bcrypt

class User:
    db = "loginFlex"
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


 
    @classmethod
    def register_user(cls,data):
        query = """
        INSERT INTO users 
        (first_name, last_name,email,password)
        VALUES
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """ 
        print('You got this!!!')
        return connectToMySQL(cls.db).query_db(query,data)
       



    @classmethod
    def get_one_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        found_user_object = cls(results[0]) 
        return found_user_object

    @classmethod
    def get_one_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) == 0:
            return None
        else:
            found_user_object = cls(results[0]) 
        return found_user_object
            

    
    @staticmethod
    def validate_registration(data):
        print(data)
        is_valid = True
        
        if len(data['first_name']) < 2:
            is_valid = False
            flash("First name must have more than 2 characters!!!!","register")
       
        if len(data['last_name']) < 2:
            is_valid = False 
            flash("Last name must be more than 2 characters!!!!","register")
        
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Invalid email address!!","register")   
        
        found_user_or_none = User.get_one_user_by_email({"email": data["email"]})
        if found_user_or_none != None:
            is_valid = False
            flash("Email is already taken","register")
        
        if len(data['password']) < 8 :
            is_valid = False
            flash('Passwords must be more than 8 characters long!!!',"register")
        
        if data['password'] != data['confirm']:
            is_valid = False      
            flash("Passwords do not match","register")
        print("complete validation")        
        return is_valid    

    @staticmethod
    def validate_login(form_data):
        print(form_data)
        is_valid = True
        
        found_user_or_none =  User.get_one_user_by_email({"email": form_data["email"]})
        if found_user_or_none == None:
            is_valid = False
            flash("Login credentials invalid","login")
        elif not bcrypt.check_password_hash(found_user_or_none.password, form_data['password']):
            is_valid = False
            flash("Login credentials invalid","login")
        return is_valid    

 
 