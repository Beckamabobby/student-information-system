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

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    section = db.relationship("Section", back_populates="teacher", uselist=False)

    def __repr__(self):
        return self.name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    section = db.relationship("Section", back_populates="course", uselist=False)

    def __repr__(self):
        return self.name

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False)
    teacher = db.relationship("Teacher", back_populates="section")
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    course = db.relationship("Course", back_populates="section")

    def __repr__(self):
        return f'period: {self.period}, teacher: {self.teacher}, course: {self.course}'

db.drop_all()
db.create_all()

tea1 = Teacher(name='Gerard')
tea2 = Teacher(name='Giles')
cor1 = Course(name='Math')
cor2 = Course(name='English')
cor3 = Course(name='Chemistry')
sec1 = Section(period=1, teacher=tea1, course=cor1)
sec2 = Section(period=2, teacher=tea2, course=cor2)
sec3 = Section(period=3, teacher=tea1, course=cor3)
stu1 = Student(first_name='Beck', last_name='Iverson')
stu1.sections.append(sec1)
stu1.sections.append(sec3)
stu2 = Student(first_name='John', last_name='Doe')
stu2.sections.append(sec1)
stu2.sections.append(sec2)

db.session.add_all([stu1])
db.session.commit()

for student in Student.query.all():
    print(student)
    print('Sections:')
    for section in student.sections:
        print(f'\t{section}')
