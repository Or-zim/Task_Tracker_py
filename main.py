from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()
my_sql_password = os.environ.get("MYSQL_PASSWORD")
name_db = 'tasks_db'






def create_db(name_db=name_db, password=my_sql_password):
    #подключается к серверу бд и создает новую бд если ее еще не было
    try:
        with connect(
            host="localhost",
            user = 'root',
            password = password,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                list_db = cursor.fetchall()
                new_list_db = [item for tuple in list_db for item in tuple]
                if name_db in new_list_db:
                    return
                else:
                    with conn.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE {name_db}")
    except Error as e:
        print(e)


def connect_db(host='localhost', name_user='root', password=my_sql_password, name_db=name_db):
    try:
        connection = connect(
            host = host,
            user = name_user,
            password = password,
            database = name_db
        )
        return connection
    except Error as e:
        print(e)
        return 

def chek_rows(cursor):
    rows = cursor.rowcount
    if rows != 0:
        print("Успешно!")
        return
    print('Введен не существующий id')



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



def delete_task(id, connect=connect_db()):
    #функция удаления задачи по id
    try:
        with connect.cursor() as cursor:
            cursor.execute('''
                            DELETE FROM task_table
                            WHERE id = %s
                            ''', (id,))
            chek_rows(cursor)
            connect.commit()
    except Error as e:
        print(e)
        return



def update_task(id, connect=connect_db()):
    #функция обновления описания задачи
    try:
        description = input('Введите новое поисание.')
        with connect.cursor() as cursor:
            cursor.execute('''
                            UPDATE task_table
                            SET description = %s
                            WHERE id = %s
                            ''', (description, id))
            chek_rows(cursor)
            connect.commit()
    except Error as e:
        print(e)
        return

def choose_task_status(id, connect=connect_db()):
    #функция отметки задачи
    try:
        print('''
1. В процессе.
2. Завершена.
3. Не выполнена.
''')
        status_key = int(input('Выберите статус задачи.(1, 2, 3): '))
        status_dict = {1: 'В процессе', 2: 'Завершена.', 3: 'Не выполнена.'}
        with connect.cursor() as cursor:
            cursor.execute('''
                            UPDATE task_table
                            SET status = %s
                            WHERE id = %s
                            ''', (status_dict[status_key], id))
            chek_rows(cursor)
            connect.commit()
    except Error as e:
        print(e) 
        return


def get_all_tasks(connect=connect_db()):
    #вывод всех задач 
    try:
        with connect.cursor() as cursor:
            cursor.execute('''
                            SELECT *
                            FROM task_table
                            ''')
            data_table = cursor.fetchall()
            for i in data_table:
                print(*i)
            connect.commit()
            return
    except Error as e:
        print(e)
        return
    
 

def get_completed_tasks(connect=connect_db()):
    #вывод выполненных задач 
    try:
        with connect.cursor() as cursor:
            cursor.execute('''
                            SELECT *
                            FROM task_table
                            WHERE status='Завершена.'
                            ''')
            data_table = cursor.fetchall()
            for i in data_table:
                print(*i)
            connect.commit()
            return
    except Error as e:
        print(e)
        return
    


def get_not_completed_tasks():
    #вывод не выполненных задач 
    pass

def get_process_tasks():
    #вывод задач в процессе
    pass


