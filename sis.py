from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sis2.db'
db = SQLAlchemy(app)

user_first_name = input('What is your first name: ')
user_last_name = input('What is your last name: ')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer, nullable=False)


db.drop_all()
db.create_all()

stu1 = Student(first_name=user_first_name, last_name=user_last_name)

sec1 = Section(period=1)

db.session.add_all([stu1, sec1])
db.session.commit()
