"""
    Simple flask app to create a server for the todo app and handle the database
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hamed.zoghi@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable = False)

    def __repr__():
        return f'<Todo id: {self.id}, decription: {self.description}>'

db.create_all()


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())
