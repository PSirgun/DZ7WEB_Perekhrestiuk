from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc

from add_db import Groups, Grades, Students, Teachers, Courses

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres', echo=False)

DBSession = sessionmaker(bind=engine)
session = DBSession()

def select_1():
    result = session.query(Students.name_stud, func.round(func.avg(Grades.grade), 2).label('avg_grade'))\
        .select_from(Grades).join(Students).group_by(Students.id_stud).order_by(desc('avg_grade')).limit(5).all()
    return result

def select_2(searh_course="Math"):
    result = session.query(
        Students.name_stud,
        Courses.name_course,
        func.round(func.avg(Grades.grade), 2))\
        .select_from(Grades)\
        .join(Students)\
        .join(Courses)\
        .filter(Courses.name_course == searh_course)\
        .group_by(Grades.id_stud, Students.name_stud, Courses.name_course)\
        .order_by(func.avg(Grades.grade).desc())\
        .limit(1).all()
    return result

def select_3(searh_course="Math"):
    result = (
        session.query(
            Groups.g_name,
            Courses.name_course,
            func.avg(Grades.grade)
        )
        .select_from(Groups)
        .join(Students)
        .join(Grades)
        .join(Courses)
        .filter(Courses.name_course == searh_course)
        .group_by(Groups.g_name, Courses.name_course)
        .all()
        
    )
    return result

def select_4():
    result = (
        session.query(
            func.round(func.avg(Grades.grade), 2)
        )
        .all()
    )
    return result

def select_5(searh_teacher='1'):
    result = (
        session.query(Teachers.name_teach, Courses.name_course)
        .select_from(Courses)
        .join(Teachers)
        .filter(Teachers.id_teach == searh_teacher)
        .all()
    )
    return result

def select_6(searh_group='group01'):
    result = (
        session.query(Students.name_stud, Students.group_name)
        .filter(Students.group_name == searh_group)
        .all()
    )
    return result

def select_7(searh_group='group01', searh_course="Math"):
    result = (
        session.query(Students.name_stud, Students.group_name, Courses.name_course, Grades.grade)
        .select_from(Grades)
        .join(Students)
        .join(Groups)
        .join(Courses)
        .filter(Groups.g_name == searh_group, Courses.name_course == searh_course)
        .all()
    )
    return result

def select_8(searh_teacher='1'):
    result = (
        session.query(Teachers.name_teach, func.round(func.avg(Grades.grade), 2))
        .select_from(Grades)
        .join(Courses)
        .join(Teachers)
        .filter(Teachers.id_teach == searh_teacher)
        .group_by(Teachers.name_teach)

        .all()
    )
    return result

def select_9(search_stud='1'):
    result = (
        session.query(Students.name_stud, Students.id_stud, Courses.name_course)
        .join(Grades, Students.id_stud == Grades.id_stud)
        .join(Courses, Grades.id_course == Courses.id_course)
        .filter(Students.id_stud == search_stud)
        .group_by(Students.name_stud, Students.id_stud, Courses.name_course)
        .all()
    )
    return result

def select_10(search_stud='1', search_teacher='1'):
    result = (
        session.query(Students.name_stud, Courses.name_course, Teachers.name_teach)
        .join(Grades, Students.id_stud == Grades.id_stud)
        .join(Courses, Grades.id_course == Courses.id_course)
        .join(Teachers, Courses.id_teach == Teachers.id_teach)
        .filter(Students.id_stud == search_stud, Teachers.id_teach == search_teacher)
        .group_by(Students.name_stud, Courses.name_course, Teachers.name_teach)
        .all()
    )
    return result


# def select():
#     courses = session.query(Courses).all()
#     for course in courses:
#         teacher = course.teacher
#         print(f"Course: {course.name_course}, Teacher: {teacher.name_teach}")

if __name__ == '__main__':
    list_select = [
        select_1(),
        select_2('Physic'),
        select_3('Physic'),
        select_4(),
        select_5('2'),
        select_6('group02'),
        select_7('group02', 'Physic'),
        select_8('2'),
        select_9('2'),
        select_10('25', '2')
    ]
    count = 1
    for sel in list_select:
        print (f'\n{count}')
        count +=1
        for i in sel:
            print (i)
    # select()


