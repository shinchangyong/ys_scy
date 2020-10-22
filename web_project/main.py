from web_project import *

@app.route("/")
def home():
    return render_template('home.html')