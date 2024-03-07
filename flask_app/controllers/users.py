from flask import render_template, redirect, session, request


from flask_app import app, bcrypt
from flask_app.models.user import User







@app.route('/') 
def home_page(): 
    if 'user_id' in session:
        redirect('/dashboard')
    return render_template("index.html")

@app.route('/dashboard')
def dashboard_page():
    
    if "user_id" not in session:
        return redirect("/") 
    
    data = {
        "id": session['user_id']
    }
    
    return render_template("dashboard.html", found_user = User.get_one_user_by_id(data))



@app.route('/register', methods=['POST'])
def register_new_user():
  
    if not User.validate_registration(request.form):
        return redirect("/")
    new_user_data = {
        
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.register_user(new_user_data)
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login_user():
    
        if not User.validate_login(request.form):
            return redirect ("/")
        email_data = {
            "email": request.form['email']
        }
        
        found_user = User.get_one_user_by_email(email_data)
        
        session["user_id"] = found_user.id
        return redirect('/dashboard')





@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/') 