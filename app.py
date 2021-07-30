from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)#, default = datetime.utcnow)
    content = db.Column(db.String(200), default = '')
    
    def __init__(self,content,created_date=None):
        self.content = content
        if created_date is None:
            created_date = datetime.utcnow()
        self.created_date = created_date


    def __repr__(self):
        return '<Task %r>' % self.id


db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)
        #new_task = Todo(content = '2019-06-29 17:08:00')
        #new_task = Todo(created_date = datetime.utcnow)
        #new_task = Todo()
        #new_task.content = task_content
        #new_task.created_date = datetime.utcnow

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')  
        except: 
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.created_date).all()
        return render_template('index.html', tasks=tasks) 


@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return  redirect('/')
    except: 
        return 'There was a problem with deleting'
@app.route('/update/<int:id>', methods = ['Get', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    #db.Column(db.DateTime, default = datetime.utcnow)

    if request.method == 'POST':
        #new_date = task.created_date 
        #update_date = datetime.utcnow
        #new_date == update_date
        #task.created_date = '2019-06-29 17:08:10' 
        task.content = request.form['content']
        #task.created_date = '2019-06-29 17:08:00'
        #task_created_date = request.form['created_date']
        #new_date = Todo(created_date = task_created_date)
        #task.created_date = 0
        #date_update = request.form['created_date']
       
        #update_date = db.Column(db.DateTime, default = datetime.utcnow)
        #new_date == update_date

        try:
            db.session.commit()
            return redirect ('/')
        except: 
            return 'Update task'

    else: 
        return render_template('update.html', task=task)



if __name__ == "__main__":  
        app.run(debug = True) 

