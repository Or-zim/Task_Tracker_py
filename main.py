from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()
my_sql_password = os.environ.get("MYSQL_PASSWORD")
name_db = 'tasks_db'

def create_db():
    #подключается к серверу бд и создает новую бд если ее еще не было
    try:
        with connect(
            host="localhost",
            user = 'root',
            password = my_sql_password,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                list_db = cursor.fetchall()
                new_list_db = []
                for i in list_db:
                    for j in i:
                        new_list_db.append(j)
                if name_db in new_list_db:
                    return
                else:
                    with conn.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE {name_db}")
    except Error as e:
        print(e)


def connect_db():
    try:
        connection = connect(
            host="localhost",
            user = 'root',
            password = my_sql_password,
            database=name_db
        )
        return connection
    except Error as e:
        print(e)
        return 


def create_table(connect=connect_db()):
    #функция создает таблицу в бд
    try:
        with connect.cursor() as cursor:
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS task_table(
                               id INT AUTO_INCREMENT PRIMARY KEY,
                               title VARCHAR(255) NOT NULL,
                               description TEXT,
                               status VARCHAR(16) NOT NULL,
                               createdAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               updatedAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                           );
                           ''')
        print('таблица успешно создана')
    except Error as e:
        print(e)
        return
    
def create_task(connect=connect_db()):
    #функция которая создает задачи
    print('Введите данные о задаче.')
    while True:
        try:
            title = input('Название: ')
            description = input('Описание: ')
            status = 'В процессе.'
            with connect.cursor() as cursor:
                cursor.execute( ''' INSERT INTO task_table (title, description, status, createdAT, updatedAT)
                                    VALUES (%s, %s, %s, NOW(), NOW())
                                ''',
                                (title, description, status)
                            )
                connect.commit()
                print('Задача успешно создана')
                return
        except Error as e:
            print(e)
            return

create_task()

def delete_task():
    #функция удаления задачи 
    pass


def update_task():
    #функция обновления задачи
    pass


def choose_task_status():
    #функция отметки задачи
    pass

def get_full_tasks():
    #вывод всех задач 
    pass

def get_completed_tasks():
    #вывод выполненных задач 
    pass

def get_not_completed_tasks():
    #вывод не выполненных задач 
    pass

def get_process_tasks():
    #вывод задач в процессе
    pass


