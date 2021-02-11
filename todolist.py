from datetime import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Some_task')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

print("1) Today's tasks", "2) Add task", "0) Exit",  sep='\n')
action = int(input())
while action != 0:
    if action == 1:
        print('\nToday:')
        rows = session.query(Table).all()
        today_tasks = list()
        for row in rows:
            if row.deadline == datetime.date(datetime.today()):
                today_tasks.append(row.task)
                print(row.task)
        if len(today_tasks) == 0:
            print('Nothing to do!')
    elif action == 2:
        task = input('\nEnter task\n')
        new_row = Table(task=task)  # deadline=datetime.strptime('01-24-2020', '%m-%d-%Y').date()
        session.add(new_row)
        session.commit()

    print("\n1) Today's tasks", "2) Add task", "0) Exit", sep='\n')
    action = int(input())

print('\nBye!')
