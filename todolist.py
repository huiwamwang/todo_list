from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column('id', Integer, primary_key=True)
    string_field = Column('task', String, default='Empty')
    date_field = Column('deadline', Date, default=datetime.today())

    def __repr__(self):
        return '{}. {}'.format(self.string_field, self.date_field)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
sess = Session()


class Todo:

    def __init__(self):
        self.main()
        self.del_dict = {}

    def read_day(self, date_):
        rows = sess.query(Table).filter(Table.date_field == date_.date())
        if rows.count() > 0:
            print('Today ' + datetime.today().strftime('%-d %b') + ':')
            for n, r in enumerate(rows, start=1):
                data = str(r).split('. ')
                print(n, data[0], sep='. ')
        elif rows.count() == 0:
            print('\nToday:\nNothing to do!')
        self.main()

    def read_week(self):
        for i in range(0, 7):
            date_ = (datetime.today() + timedelta(days=i)).strftime('%A %-d %b')
            date1 = datetime.today() + timedelta(days=i)
            rows = sess.query(Table).filter(Table.date_field == date1.date())
            print('\n' + date_)
            if rows.count() > 0:
                for n, r in enumerate(rows, start=1):
                    data = str(r).split('. ')
                    print(n, data[0], sep='. ')
            elif rows.count() == 0:
                print('Nothing to do!')

        self.main()

    def read_all(self, text, param):
        rows = sess.query(Table).order_by(Table.date_field).all()
        self.del_dict = {}
        if rows:
            print(text)
            for n, r in enumerate(rows, start=1):
                data = str(r).split('. ')
                print(n, data[0], datetime.fromisoformat(data[1]).strftime('%-d %b'), sep='. ')
                self.del_dict[n] = data[0]
        else:
            print('\nToday:\nNothing to do!')
        if param == 'readall':
            self.main()
        elif param == 'delete':
            u_inp = int(input())
            sess.query(Table).filter(Table.string_field == self.del_dict[u_inp]).delete()
            sess.commit()
            print('The task has been deleted!')
            self.main()

    def read_missed(self):
        rows = sess.query(Table).filter(Table.date_field < datetime.today().date()).order_by(Table.date_field)
        if rows.count() > 0:
            print('Missed tasks:')
            for n, r in enumerate(rows, start=1):
                data = str(r).split('. ')
                print(n, data[0], datetime.fromisoformat(data[1]).strftime('%-d %b'), sep='. ')
        elif rows.count() == 0:
            print('\nToday:\nNothing to do!')
        self.main()

    def write_data(self):
        task = input('Enter task\n')
        date = input('Enter deadline\n')
        new_row = Table(string_field=task, date_field=datetime.fromisoformat(date))
        sess.add(new_row)
        sess.commit()
        print('The task has been added')
        self.main()

    def main(self):
        user_input = input("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task"
                           "\n6) Delete task\n0) Exit\n")
        if user_input == '1':
            self.read_day(datetime.today())
        elif user_input == '2':
            self.read_week()
        elif user_input == '3':
            self.read_all(text='All tasks:', param='readall')
        elif user_input == '4':
            self.read_missed()
        elif user_input == '5':
            self.write_data()
        elif user_input == '6':
            self.read_all(text='Choose the number of the task you want to delete:', param='delete')
        elif user_input == '0':
            print('Bye!')
            exit()


Todo()
