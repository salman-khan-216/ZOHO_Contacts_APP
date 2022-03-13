import email
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    secretkey = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.secretkey

@login_manager.user_loader
def load_user(email):
    return User.query.get(str(email))

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/display")
def display():
    return render_template("display.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST" :
        email = request.form.get("email")
        password = request.form.get("password")
        secretkey = request.form.get("secretkey")
        user = User(email=email,password=password,secretkey=secretkey)
        db.session.add(user)
        db.session.commit()
        flash("User Has Been Registered Successfully","Success")
        return redirect('/login')
    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and password==user.password:
            login_user(user)
            return redirect('/display')
        else:
            flash("Invalid credentials", "warning")
            return redirect("/login")
    return render_template("login.html")

if __name__ == "__main__" :
    app.run(debug=True)
