from datetime import datetime, timedelta
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

today = datetime.today()

print("1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Add task", "0) Exit",  sep='\n')
action = int(input())
while action != 0:
    if action == 1:
        print(f'\nToday {today.day} {today.strftime("%b")}:')
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        count = 1
        if len(rows) != 0:
            for row in rows:
                print(f'{count}. {row.task}')
                count += 1
        else:
            print('Nothing to do!')
        print()
    elif action == 2:
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        curr_day = today
        rows = session.query(Table).order_by(Table.deadline).all()
        for i in range(7):
            print(f'\n{weekdays[curr_day.weekday()]} {curr_day.day} {curr_day.strftime("%b")}')
            rows = session.query(Table).filter(Table.deadline == curr_day.date()).order_by(Table.deadline).all()
            count = 1
            if len(rows) != 0:
                for row in rows:
                    print(f'{count}. {row.task}')
                    count += 1
            else:
                print('Nothing to do!')
            curr_day += timedelta(days=1)
        print()
    elif action == 3:
        print('\nAll tasks:')
        rows = session.query(Table).order_by(Table.deadline).all()
        count = 1
        if len(rows) != 0:
            for row in rows:
                print(f'{count}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
                count += 1
        else:
            print('Nothing to do!')
        print()
    elif action == 4:
        task = input('\nEnter task\n')
        deadline = input('Enter deadline\n')
        new_row = Table(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')

    print("1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Add task", "0) Exit",  sep='\n')
    action = int(input())

print('\nBye!')
