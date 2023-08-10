from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),nullable=False)
    note = db.Column(db.String(200),nullable=False)
    due_date = db.Column(db.DateTime,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now,nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now,nullable=False)


