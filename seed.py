"""

Наповнюю таблиці

"""
from faker import Faker
import random
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import sessionmaker

from add_db import Groups, Grades, Students, Teachers, Courses


fake = Faker()
ALL_GRADES = ['5','4','3','2','1','0'] 
ALL_GROUPS = ['group01', 'group02', 'group03']
ALL_COURSES = ['Math', 'Physic', 'Music', 'Sport', 'History']

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres', echo=False)

DBSession = sessionmaker(bind=engine)
session = DBSession()





def seed(num_studs=50, num_teachers=3):
    
    for group_name in ALL_GROUPS:
        ins = Insert(Groups).values(g_name=group_name).on_conflict_do_nothing()
        session.execute(ins)
    session.commit()

#-----------------------------------------------------------------------------------------------------------------------------   
    
    for _ in range(num_studs):
            student_name = fake.name()
            random_group = random.choice(ALL_GROUPS)
            students_query = Students(name_stud=student_name, group_name=random_group)
            session.add(students_query)
    session.commit()

#-----------------------------------------------------------------------------------------------------------------------------   
    teachers_list = []        
    
    for _ in range (num_teachers):
        teacher_degree = random.choice(['Professor', 'Doctor'])
        teacher_name = (f'{teacher_degree} {fake.last_name()}',)
        teachers_list.append(teacher_name)
    
    teachers_query = [Teachers(name_teach=t_name) for t_name in teachers_list]
    session.add_all(teachers_query)
    session.commit()

#-----------------------------------------------------------------------------------------------------------------------------   

    for c in ALL_COURSES:
         random_teacher = random.randint(1, num_teachers)
         course_query = Courses(name_course=c, id_teach=random_teacher)
         session.add(course_query)
         
    session.commit()
#-----------------------------------------------------------------------------------------------------------------------------   
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    for stud_id in range(1, num_studs+1):
        for course_id in range(1, len(ALL_COURSES)):
            grade = random.choice(ALL_GRADES)
            num_grades = random.randint(1, 5)
            for _ in range(num_grades+1):
                random_date = fake.date_between(start_date=start_date, end_date=end_date)
                grade_query = Grades(id_stud=stud_id, id_course=course_id, grade=grade, date_received=random_date)
                session.add(grade_query)

    session.commit()
  


def del_seed():
     session.query(Grades).delete()
     session.query(Students).delete()
     session.query(Groups).delete()
     session.query(Courses).delete()
     session.query(Teachers).delete()
    
     session.commit()


if __name__ == '__main__':
    del_seed()
    seed()
    print('all ok')

    session.close()