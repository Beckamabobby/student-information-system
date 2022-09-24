from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sis2.db'
db = SQLAlchemy(app)

student_sections = db.Table('student_sections',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),  # Foreign key refers to item in another table
    db.Column('section_id', db.Integer, db.ForeignKey('section.id'), primary_key=True)
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    sections = db.relationship('Section', secondary=student_sections, lazy='subquery',
                               backref='students')

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'period {self.period}'

db.drop_all()
db.create_all()

sec1 = Section(period=1)
sec2 = Section(period=2)
sec3 = Section(period=3)
stu1 = Student(first_name='Beck', last_name='Iverson')
stu1.sections.append(sec1)
stu1.sections.append(sec3)
stu2 = Student(first_name='John', last_name='Doe')
stu2.sections.append(sec1)
stu2.sections.append(sec2)

db.session.add_all([stu1, stu2, sec1, sec2, sec3])
db.session.commit()

for student in Student.query.all():
    print(student)
    print('Sections:')
    for section in student.sections:
        print(f'\t{section}')