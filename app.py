from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Todo.db"
db= SQLAlchemy(app)

class TodoDB(db.Model):
    Sno= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200), nullable= False)
    desc= db.Column(db.String(500), nullable= False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self)-> str:
        return f"{self.Sno}-{ self.title}"

@app.route('/', methods =['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title=request.form['title']
        desc= request.form['desc']
        todo = TodoDB(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=TodoDB.query.all()
    return render_template('index.html', alltodo= alltodo)
    # return 'Hello, World!'

@app.route('/products')
def products():
    return 'This is products page. renders 2'

# @app.route('/show')
# def show():
#     alltodo=TodoDB.query.all()
#     print(alltodo)
#     return 'This is products page. renders 2'

@app.route('/update/<int:sno>', methods =['GET', 'POST'])
def update(sno):
    if request.method =="POST":
        title=request.form['title']
        desc= request.form['desc']
        todo=TodoDB.query.filter_by(Sno=sno).first()
        todo.title= title
        todo.desc= desc
        db.session.add(todo)
        db.session.commit()
    todo=TodoDB.query.filter_by(Sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=TodoDB.query.filter_by(Sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    # app.run(debug=True) #to change port ---> app.run(debug=True, port=8000)
    with app.app_context():
        db.create_all()
    app.run(debug=True)