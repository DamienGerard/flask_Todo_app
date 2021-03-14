from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
  tasks =[]
  if(request.method=='POST'):
    task_content = request.form['content']
    new_task = Todo(content = task_content)

    try:
      db.session.add(new_task)
      db.session.commit()
    except:
      return "Oops, there was an error while adding your task. Please, try again."

    return redirect('/')
  #elif(request.method=='GET'):
  
  tasks = Todo.query.order_by(Todo.date_created).all()

  return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)

  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return "Oops, there was an error while deleting that task. Please, try again."

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
  task = Todo.query.get_or_404(id)
  if request.method == 'POST':
    task.content = request.form['content']

    try:
      db.session.commit()
    except:
      return "Oops, there was an error while updating that task. Please, try again."

    return redirect('/')
  else:
    return render_template('update.html', task = task)


if __name__ == "__main__":
  app.run(debug=True)