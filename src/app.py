"""
    Simple flask app to create a server for the todo app and handle the database
"""
import sys
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hamed.zoghi@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable = False)
    completed = db.Column(db.Boolean, nullable=False, default = False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__():
        return f'<Todo id: {self.id}, decription: {self.description}, completed: {self.completed}, list_id = {self.list_id}>'

class TodoList(db.Model):
    __tablename__='todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__():
        return f'<TodoList id: {self.id}, name: {self.name}>'

@app.route('/todos/create', methods = ['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['description'] = todo.description
        body['completed'] = todo.completed
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods = ['POST'])
def set_completed_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo =  Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('index'))

@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def delete_todo(todo_id):
    error = False
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:        
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify({'success': True})


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
    active_list = TodoList.query.get(list_id),
    lists = TodoList.query.order_by('id').all(), 
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())


@app.route('/lists/create')
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todo_list = TodoList(name=name)
        db.session.add(todo_list)
        db.session.commit()
        body['id'] = todo_list.id
        body['name'] = todo_list.name
    except: 
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(400)
    else:
        return jsonify(body)

    


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))
