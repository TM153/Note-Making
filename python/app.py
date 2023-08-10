from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:NicIndia13@localhost/mynotes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
from models import db,Notes
db.init_app(app)
with app.app_context():
   db.create_all()
import mysql.connector
conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='NicIndia13',
        database='mynotes'
    )


@app.route('/')
def home():
    notes = Notes.query.all()
    return render_template('mynotes.html',notes=notes)

@app.route('/mynotes')
def display():
        notes = Notes.query.all()
        return render_template('mynotes.html',notes=notes)

@app.route('/notes',methods=['GET','POST'])
def notes():
    if request.method == 'POST':
        name = request.form.get('name')
        note = request.form.get('note')
        due_date = request.form.get('due_date')        
        new_note = Notes(name=name,note=note,due_date=due_date)
        db.session.add(new_note)
        db.session.commit()
        notes = Notes.query.all()
        return render_template('mynotes.html',notes=notes)
    else:
        notes = Notes.query.all()  
        return render_template('mynotes.html',notes=notes)

@app.route('/retrieve',methods=['GET','POST'])
def retrieve():
    if request.method == 'POST':
        id = request.form.get('id')
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        query = Notes.query
        if id:
            query = query.filter(Notes.id == id)
        if title:
            query = query.filter(Notes.name.ilike(f'%{title}%'))          
        if due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
            query = query.filter(Notes.due_date <= due_date)    
        retrieved = query.all()
        return render_template('mynotes.html', retrieved=retrieved ,notes = Notes.query.all())
    return render_template('mynotes.html',notes = Notes.query.all())

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        if id:
            note = Notes.query.get(id)
            db.session.delete(note)
            db.session.commit()
        return render_template('mynotes.html',notes = Notes.query.all())
    return render_template('mynotes.html',notes = Notes.query.all())

@app.route('/edit',methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        id = request.form.get('id')
        if id:
            note = Notes.query.filter_by(id = id).first()
            return render_template('mynotes.html',update=1,id=note.id,name=note.name,note=note.note,due_date=note.due_date,notes=Notes.query.all())
        else:
            return render_template('mynotes.html',update=0,notes = Notes.query.all())
    return render_template('mynotes.html',notes = Notes.query.all())

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        id = request.form.get('id')
        title = request.form.get('name')
        desc = request.form.get('note')
        due_date = request.form.get('due_date') 
        note = Notes.query.get(id)      
        note.name = title
        note.note = desc
        note.due_date = due_date
        db.session.commit()
        return render_template('mynotes.html',notes = Notes.query.all())
    return render_template('mynotes.html',notes = Notes.query.all())

if __name__ == '__main__':
    app.run(debug=True)