from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    body=db.Column(db.String(300),nullable=False)
    created_at=db.Column(db.DateTime,nullable=False,default=datetime.now(pytz.timezone("Asia/Tokyo")))


@app.route("/",methods=["GET"])
def index():
    posts=Post.query.all()
    return render_template("index.html",posts=posts)

@app.route("/article1")
def article1():
    return render_template("article1.html")

@app.route("/article2")
def article2():
    return render_template("article2.html")

@app.route("/create",methods=["GET","POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        
        post = Post(title=title,body=body)
        
        db.session.add(post)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("create.html")

@app.route("/<int:id>/update",methods=["GET","POST"]) 
def update(id):
    post=Post.query.get(id)
    if request.method == "GET":
        return render_template("update.html",post=post)
    else:
        post.title = request.form.get("title")
        post.body = request.form.get("body")
        db.session.commit()
        return redirect("/")

@app.route("/<int:id>/delete",methods=["GET"])
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")

@app.route('/up/',methods=['POST'])
def up_post():
    f=request.files.get('image')
    filename=secure_filename(f.filename)
    filepath='imagebox/image/'+filename
    f.save(filepath)
    return render_template('index.html',title='Form Sample(post)',message='アップロードされた画像({})'.format(filename),flag=True,image_name=filename)

if __name__ == '__main__':
    app.run(debug=True)