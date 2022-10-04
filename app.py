from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Todo(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    decs=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__ (self)->str:
        return f"{self.Sno} - {self.title}"

@app.route('/',methods=['GET', 'POST'])
def hello_world():

    if request.method=="POST":
        title=request.form['title']
        desc=request.form['decs']
        todo= Todo(title=title, decs=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()

    return render_template("index.html",alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    data=Todo.query.get(sno)
    # print(data.title)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')
    
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['decs']
        data=Todo.query.filter_by(Sno=sno).first()
        data.title=title
        data.decs=desc
        db.session.add(data)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(Sno=sno).first()
    return render_template('update.html',todo=todo)
    

if __name__=="__main__":
    app.run(debug=True, port=8000)

