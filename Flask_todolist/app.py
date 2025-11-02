from todolist import create_app
from flask import  render_template 
app = create_app()
@app.route("/")
def login():
    return render_template("login.html")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/Logout")
def logout():
    return render_template("signup.html")
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=911)