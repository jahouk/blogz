from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/', methods=['GET'])
def index():
    return redirect('/blog')


@app.route('/blog', methods=['GET'])
def blog():
    view = 'default'
    blogs = []
    if request.args:
        id = request.args.get('id')
        blogs.append(Blog.query.get(id))
        view = 'single'
    else:
        blogs = Blog.query.all()
    return render_template('blog.html', page_title='Build-A-Blog', blogs=blogs, view=view)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title = ""
    title_error = ""
    body = ""
    body_error = ""

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not len(title) > 0:
            title_error = "Title must contain a value"
            
        if not len(body) > 0:
            body_error = "Body must contian a value"
         
        if not(title_error) and not(body_error):
            new_post = Blog(title = title, body = body)
            db.session.add(new_post)
            db.session.commit()
            db.session.refresh(new_post)
            return redirect('/blog?id='+ str(new_post.id))            
    
    return render_template('newpost.html', page_title = "Add A Post", title = title, 
        title_error = title_error, body = body, body_error = body_error)

if __name__ == '__main__':
    app.run()

