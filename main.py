from mysql.connector import connect, Error
import os
from dotenv import load_dotenv
from tabulate import tabulate
load_dotenv()
my_sql_password = os.environ.get("MYSQL_PASSWORD")
name_db = 'tasks_db'
name_table = 'task_table'

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
    #подключается к сущесвующей бд
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
    #выполняет проверку на ненулевое количество записей
    rows = cursor.rowcount
    if rows != 0:
        print("Успешно!")
        return
    print('Введен не существующий id')

def create_table(connect=connect_db(), name_tab=name_table):
    #функция создает таблицу в бд
    try:
        with connect.cursor() as cursor:
            cursor.execute(f'''
                           CREATE TABLE IF NOT EXISTS {name_tab}(
                               id INT AUTO_INCREMENT PRIMARY KEY,
                               title VARCHAR(255) NOT NULL,
                               description TEXT,
                               status VARCHAR(16) NOT NULL,
                               createdAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               updatedAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                           );
                           ''')
            connect.commit()
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
        description = input('Введите новое описание.')
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
            title_table = [i[0] for i in cursor.description]
            print(tabulate(data_table, headers=title_table, tablefmt="grid", stralign="center"))
            connect.commit()
            return
    except Error as e:
        print(e)
        return



def main():
    while True:
        print("\nМеню трекера задач:")
        print("1. Создать задачу")
        print("2. Удалить задачу")
        print("3. Обновить задачу")
        print("4. Отметить задачу")
        print("5. Показать все задачи")
        print("6. Выход")
        try:
            choice = int(input("Выберите действие: "))
        except:
            print('Введите коректные данные!!!')
            continue
        
        if choice == 13062006:
            print('\nЭто функционал разработчика.')
            print('1. Создать бд')
            print('2. Изменить подключение к бд')
            print('3. Создать таблицу')
            try:
                dev_choice = int(input("Выберите действие: "))
                if dev_choice == 1:
                    name = input('Введите название бд: ')
                    create_db(name_db=name)
                    print('Бд успешно создана')
                elif dev_choice == 2:
                    name = input('Введите название бд: ')
                    connect_db(name_db=name)
                elif dev_choice == 3:
                    name = input('Введите название таблицы: ')
                    create_table(name_tab=name)

            except:
                print('Введите коректные данные!!!')
                continue
            
            
        elif choice == 1:
            create_task()
            
        elif choice == 2:
            try:
                id = int(input("Введите id задачи: "))
                delete_task(id)
            except:
                print('Введите коректные данные!!!')
                
        elif choice == 3:
            try:
                id = int(input("Введите id задачи: "))
                update_task(id)
            except:
                print('Введите коректные данные!!!')
                
        elif choice == 4:
            try:
                id = int(input("Введите id задачи: "))
                choose_task_status(id)
            except:
                print('Введите коректные данные!!!')
        elif choice == 5:
            get_all_tasks()
            
        elif choice == 6:
            break
        
        elif choice > 6:
            print('Введите коректные данные!!!')
        
if __name__ ==  "__main__":
    main()
