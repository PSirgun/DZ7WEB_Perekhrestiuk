from sqlalchemy import create_engine, ForeignKey, Date, Integer, String, Column, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, relationship
from datetime import date
from typing import List
engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres', echo=True)

DBSession = sessionmaker(bind=engine)
session = DBSession()


class Base(DeclarativeBase):
    pass

class Groups(Base):
    __tablename__ = "groups"
    g_name: Mapped[str] = mapped_column(primary_key=True)
    stud: Mapped[list['Students']] = relationship(back_populates= 'groups')

class Students(Base):
    __tablename__ = 'students'
    id_stud: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_stud: Mapped[str]
    group_name: Mapped[str] = mapped_column('group_name', ForeignKey('groups.g_name'))
    groups: Mapped['Groups'] = relationship(back_populates= 'stud')
    grade: Mapped['Grades'] = relationship(back_populates= 'student')

class Teachers(Base):
    __tablename__ = 'teachers'
    id_teach: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_teach: Mapped[str]
    course: Mapped[List['Courses']] = relationship(back_populates="teacher")
    

class Courses(Base):
    __tablename__ = 'courses'
    id_course: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_course: Mapped[str]
    id_teach: Mapped[str] = mapped_column('id_teach', ForeignKey('teachers.id_teach'))
    teacher: Mapped["Teachers"] = relationship(back_populates='course')



class Grades(Base):
    __tablename__ = 'grades'
    count: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_stud: Mapped[int] = mapped_column('id_stud', ForeignKey('students.id_stud'))
    id_course: Mapped[int] = mapped_column('id_course', ForeignKey('courses.id_course'))
    grade: Mapped[int]
    date_received: Mapped[date]
    student: Mapped[list["Students"]] = relationship(back_populates='grade')


def init_bd(engine):
    Base.metadata.create_all(engine)

def drop_bd(engine):
    Base.metadata.drop_all(engine, checkfirst=True)



if __name__ == '__main__':
    drop_bd(engine)
    init_bd(engine)

