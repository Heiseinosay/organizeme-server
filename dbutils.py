from mysql.connector import (connection)
from mysql.connector import Error

import secrets
import string

# DB CONNECTION
def connect_to_db():
    try:
        print("Attempting to connect...")

        # First method
        mysqldb = connection.MySQLConnection(
            # user='root', 
            # password='HelloWorld#,12345',                   
            # host='localhost',
            # database='organizeme' # Use Existing Database
            user='root',
            password='vRbegrxYKNkDNwQvoByWSEylhwWGSJHU',
            host='viaduct.proxy.rlwy.net',
            database='railway',
            port=41816  
        )

        print("Connection successful!")
        # Cursor
        cursor = mysqldb.cursor()

        return mysqldb, cursor

    except Error as e:
        print(f"Error: {e}")


# CREATE AN ACCOUNT
def create_account(first_name, last_name, email, password):
    mysqldb, cursor = connect_to_db()
    try:

        read_query = 'SELECT * FROM users WHERE Email = %s'
        cursor.execute(read_query, (email, ))
        result = cursor.fetchall()
        if (len(result) >= 1):
            return False
        
        insert_query = ('INSERT INTO users(FirstName, LastName, Email, Password) VALUES(%s, %s, %s, %s)') 
        record = (first_name, last_name, email, password)
        cursor.execute(insert_query, record)

        mysqldb.commit()
        # print("Successfully inserted!")
        return {'status' : 'success'}
    except Error as e:
            print(f"Error in inserting: {e}")
            return {'status' : 'failed'}
    finally:
        mysqldb.close()


# LOGIN
def login_auth(mail, password):
    mysqldb, cursor = connect_to_db()
    try:
        
        read_query = 'SELECT * FROM users WHERE Email = %s AND Password = %s'
        cursor.execute(read_query, (mail, password))
        result = cursor.fetchall()
        # print(len(result))

        if (len(result) == 1):
            return result
        else:
            return False

        
    except Error as e:
            print(f"Error in inserting: {e}")
    finally:
        mysqldb.close()


# SELECT ALL SUBJECT
def select_all_subjects(uid):
    mysqldb, cursor = connect_to_db()
    try:
        read_query = 'SELECT * FROM courses WHERE UserID = %s'
        cursor.execute(read_query, (uid,))
        result = cursor.fetchall()

        return result

        
    except Error as e:
            print(f"Error in inserting: {e}")
    finally:
        mysqldb.close()


# INSERT SUBJECT
def insert_subject(uid, subjectName):
    mysqldb, cursor = connect_to_db()
    try:
        # CHECK IF SUBJECT EXIST
        read_query = 'SELECT * FROM courses WHERE UserID = %s AND SubjectName = %s'
        cursor.execute(read_query, (uid, subjectName))
        result = cursor.fetchall()

        if (len(result) > 0):
            return {'status' : False}

        insert_query = ('INSERT INTO courses(UserID, SubjectName, LastUpdated, TaskCountOverAll) VALUES(%s, %s, curdate(), 0)') 
        record = (uid, subjectName)
        cursor.execute(insert_query, record)

        mysqldb.commit()
        print("Successfully inserted!")
        return {'status' : True}
    except Error as e:
            print(f"Error in inserting: {e}")
            return {'status' : 'failed'}
    finally:
        mysqldb.close()


# LOAD SUBJECT NAME
def fetch_subject_name(sid):
    mysqldb, cursor = connect_to_db()
    try:
        read_query = 'SELECT SubjectName FROM courses WHERE SubjectID = %s'
        cursor.execute(read_query, (sid,))
        result = cursor.fetchone()

        return { 'data': result }
    except Error as e:
        print(f"Error in updating: {e}")
        return { 'data': False }
    finally:
        mysqldb.close()



# EDIT SUBJECT NAME
def edit_subject_name(sid, subjectName):
    mysqldb, cursor = connect_to_db()
    try:

        read_query = 'SELECT * FROM courses WHERE SubjectName = %s'
        cursor.execute(read_query, (subjectName,))
        result = cursor.fetchall()

        if (len(result) > 0):
            return { 'status': False }

        update_query = "UPDATE courses SET SubjectName=%s, LastUpdated=curdate() WHERE SubjectID = %s"
        cursor.execute(update_query, (subjectName, sid))
        mysqldb.commit()

        return { 'status': True }
    except Error as e:
        print(f"Error in updating: {e}")
        return { 'status': False }
    finally:
        mysqldb.close()


# DELETE SUBJECT
def delete_subject_name(sid):
    mysqldb, cursor = connect_to_db()
    try:
        delete_query = "DELETE FROM courses WHERE SubjectID = %s"
        cursor.execute(delete_query, (sid,))
        mysqldb.commit()

        return { 'status': True }
    except Error as e:
        print(f"Error in updating: {e}")
        return { 'status': False }
    finally:
        mysqldb.close()


# INSERT TASK
from datetime import datetime, timedelta
def add_task(uid, sid, title, description, dueDate, reminder, priority, status):
    mysqldb, cursor = connect_to_db()
    try:
        # READ OVER ALL MADE TASKS
        read_query = 'SELECT TaskCountOverAll FROM courses WHERE SubjectID = %s'
        cursor.execute(read_query, (sid,))
        result = cursor.fetchone()
        
        # UPDATE TASK
        update_query = "UPDATE courses SET TaskCountOverAll=%s WHERE SubjectID = %s"
        cursor.execute(update_query, (result[0] + 1, sid))
        mysqldb.commit()
        

        # CALCULATE THE REMINDER DATE
        reminder_days = int(reminder) 
        due_date_obj = datetime.strptime(dueDate, "%Y-%m-%dT%H:%M") 
        reminder_date_obj = due_date_obj - timedelta(days=reminder_days)  
        reminder_date = reminder_date_obj.strftime("%Y-%m-%d %H:%M:%S")  

        print(reminder_date)

        chars = string.ascii_letters + string.digits  # Letters and numbers
        key_length = 12  # Length of the primary key
 
        random_key = ''.join(secrets.choice(chars) for _ in range(key_length))

        print("Random key: ", random_key)

        # INSERT TASK
        new_due_date = datetime.strptime(dueDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
        task_id = str(uid) + random_key
        print(task_id, uid, sid, title, new_due_date, description, priority, reminder_date, status)

        insert_query = "INSERT INTO task (TaskID, UserID, SubjectID, TaskTitle, DateCreated, DueDate, Description, Priority, Reminder, ReminderDate, Status, isAlertedDue, isAlertedReminder, isAlertedStart) VALUES (%s, %s, %s, %s, curdate(), %s, %s, %s, %s, %s, %s, 0, 0 ,0)"
        record = (task_id, uid, sid, title, new_due_date, description, priority, reminder, reminder_date, status)
        cursor.execute(insert_query, record)
        mysqldb.commit()
        
        print("Success!")

        return { 'status': True }
    except Error as e:
        print(f"Error in updating: {e}")
        return { 'status': False }
    finally:
        mysqldb.close()


# SELECT ALL SUBJECT TASKS
def select_subject_task(uid, sid):
    mysqldb, cursor = connect_to_db()
    try:
        read_query = 'SELECT * FROM task WHERE UserID = %s AND SubjectID = %s ORDER BY Priority DESC, DueDate ASC'
        cursor.execute(read_query, (uid, sid))
        result = cursor.fetchall()

        return { 'data': result }
    except Error as e:
        print(f"Error in updating: {e}")
        return { 'data': False }
    finally:
        mysqldb.close()


# UPDATE TASk
def update_selected_task(tid, uid, sid, title, description, dueDate, reminder, priority, status):
    mysqldb, cursor = connect_to_db()
    try:
        # REFORMAT DATE
        new_due_date = datetime.strptime(dueDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")

        # CALCULATE THE REMINDER DATE
        reminder_days = int(reminder) 
        due_date_obj = datetime.strptime(dueDate, "%Y-%m-%dT%H:%M") 
        reminder_date_obj = due_date_obj - timedelta(days=reminder_days)  
        reminder_date = reminder_date_obj.strftime("%Y-%m-%d %H:%M:%S")  

        # UPDATE TASK
        update_query = "UPDATE task SET TaskTitle=%s, DueDate=%s, Description=%s, Priority=%s, Reminder=%s, ReminderDate=%s, Status=%s WHERE TASKID=%s AND UserID=%s AND SubjectID = %s"
        cursor.execute(update_query, (title, new_due_date, description, priority, reminder, reminder_date, status, tid, uid, sid))
        mysqldb.commit()


        return { 'status': True }
    except Error as e:
        print(f"Error in updating: {e}")
        return { 'status': False }
    finally:
        mysqldb.close()



# DELETE TASK
def delete_task_name(tid, uid, sid):
    mysqldb, cursor = connect_to_db()
    try:
        delete_query = "DELETE FROM task WHERE TaskID=%s AND UserID=%s AND SubjectID = %s"
        cursor.execute(delete_query, (tid, uid, sid))
        mysqldb.commit()

        return { 'status': True }
    except Error as e:
        print(f"Error in updating: {e}")
        return { 'status': False }
    finally:
        mysqldb.close()


def task_accomplished(tid, uid, sid):
    mysqldb, cursor = connect_to_db()
    try:
        # INSERT TO ACCOMPLISH TABLE
        insert_query = """
            INSERT INTO completed (UserID, SubjectID, TaskID, SubjectName, TaskTitle, Description, Created, DueDate, CompletionDate)
            SELECT t.UserID, t.SubjectID, t.TaskID, c.SubjectName, t.taskTitle, t.Description, t.DateCreated, t.DueDate, curdate()
            FROM task as t
            INNER JOIN courses AS c
            ON t.subjectID = c.subjectID
            WHERE t.subjectID = %s AND t.taskID = %s AND t.UserID = %s;
            """
        print("im here")
        record = (sid, tid, uid)
        cursor.execute(insert_query, record)

        print(cursor)

        # DELETE FROM TASK
        delete_query = "DELETE FROM task WHERE TaskID=%s AND UserID=%s AND SubjectID = %s"
        cursor.execute(delete_query, (tid, uid, sid))
        mysqldb.commit()

        return { 'status': True }
    except Error as e:
        print(f"Error in updating: {e}")
        return { 'status': False }
    finally:
        mysqldb.close()


def select_all_accomplished(uid):
    mysqldb, cursor = connect_to_db()
    try:
        read_query = 'SELECT * FROM completed WHERE UserID = %s'
        cursor.execute(read_query, (uid,))
        result = cursor.fetchall()

        return result

        
    except Error as e:
            print(f"Error in inserting: {e}")
    finally:
        mysqldb.close()


def calendar_task(uid):
    mysqldb, cursor = connect_to_db()
    try:
        read_query = 'SELECT * FROM task WHERE UserID = %s'
        cursor.execute(read_query, (uid,))
        result = cursor.fetchall()

        return result

        
    except Error as e:
            print(f"Error in inserting: {e}")
    finally:
        mysqldb.close()


def insert_notification(uid):
    mysqldb, cursor = connect_to_db()
    try:
        #! OVERDUE
        read_query = '''
            SELECT UserID, TaskID, TaskTitle, DueDate
            FROM task
            WHERE dueDate <= now() AND
            isAlertedDue = 0 AND
            Userid = %s
        '''
        cursor.execute(read_query, (uid, ))
        result = cursor.fetchall()

        for i in range(0, len(result)):
            # print("overdue: ", result[i])
            insert_query = "INSERT INTO notifications (UserID, TaskID, TaskTitle, AlertType, DueDate) VALUES(%s, %s, %s, 'overdue', %s) "
            record = (result[i][0], result[i][1], result[i][2], result[i][3])
            # print("RECORD: ", record)
            cursor.execute(insert_query, record)

            # UPDATE ALERTDUE
            update_query = """
                UPDATE task SET isAlertedDue = 1 
                WHERE taskID = %s;
            """
            cursor.execute(update_query, (result[i][1], ))

        
        #! REMINDER
        read_query = '''
            SELECT UserID, TaskID, TaskTitle, DueDate
            FROM task
            WHERE reminderDate <= now() AND
            isAlertedReminder= 0 AND
            UserID = %s;
        '''
        cursor.execute(read_query, (uid, ))
        result = cursor.fetchall()

        for i in range(0, len(result)):
            print("overdue: ", result[i])
            insert_query = "INSERT INTO notifications (UserID, TaskID, TaskTitle, AlertType, DueDate) VALUES(%s, %s, %s, 'reminder', %s) "
            record = (result[i][0], result[i][1], result[i][2], result[i][3])
            # print("RECORD: ", record)
            cursor.execute(insert_query, record)

            # UPDATE ALERTDUE
            update_query = """
                UPDATE task SET isAlertedReminder = 1 
                WHERE taskID = %s;
            """
            cursor.execute(update_query, (result[i][1], ))

        #! START
        read_query = '''
            SELECT UserID, TaskID, TaskTitle, DueDate
            FROM task
            WHERE 
                DATE_ADD(DateCreated, INTERVAL 2 DAY) <= NOW() 
                AND status = 'Not Started'
                AND isAlertedStart = 0
                AND UserID = %s;
        '''
        cursor.execute(read_query, (uid, ))
        result = cursor.fetchall()

        for i in range(0, len(result)):
            print("overdue: ", result[i])
            insert_query = "INSERT INTO notifications (UserID, TaskID, TaskTitle, AlertType, DueDate) VALUES(%s, %s, %s, 'not started', %s) "
            record = (result[i][0], result[i][1], result[i][2], result[i][3])
            # print("RECORD: ", record)
            cursor.execute(insert_query, record)

            # UPDATE ALERTDUE
            update_query = """
                UPDATE task SET isAlertedStart = 1 
                WHERE taskID = %s;
            """
            cursor.execute(update_query, (result[i][1], ))

        mysqldb.commit()

        return result

        
    except Error as e:
            print(f"Error in inserting: {e}")
            return { 'status': False }
    finally:
        mysqldb.close()


def get_user_summary(uid):
    mysqldb, cursor = connect_to_db()
    try:
        overdue = 0
        completed = 0
        pending = 0

        # OVERDUE
        read_query = """
            SELECT COUNT(*) 
            FROM task
            WHERE UserID = %s AND
            DueDate <= now();
        """
        cursor.execute(read_query, (uid, ))
        result = cursor.fetchone()
        overdue = result[0]

        # TOTAL ACCOMPLISHED
        read_query = """
            SELECT COUNT(*) 
            FROM completed
            WHERE UserID = %s
        """

        cursor.execute(read_query, (uid, ))
        result = cursor.fetchone()
        completed = result[0]

        # PENDING
        read_query = """
            SELECT COUNT(*) 
            FROM task
            WHERE UserID = %s
        """
        cursor.execute(read_query, (uid, ))
        result = cursor.fetchone()
        pending = result[0]
        # print("My result: ", result[0])


        return { "overdue": overdue, "completed": completed, "pending": pending }
    except Error as e:
        print(f"Error in summary: {e}")
        return { 'data': False }
    finally:
        mysqldb.close()

def get_user_notification(uid):
    mysqldb, cursor = connect_to_db()
    try:
        read_query = """
                SELECT *
                FROM notifications
                WHERE UserID = %s
                ORDER BY NotificationID DESC
            """
        cursor.execute(read_query, (uid,))
        result = cursor.fetchall()

        return result

        
    except Error as e:
            print(f"Error in inserting: {e}")
    finally:
        mysqldb.close()


def search_item(uid, searchTerm):
    mysqldb, cursor = connect_to_db()
    try:
        read_query = """
            SELECT * 
            FROM task
            WHERE userId = %s AND (TaskTitle like %s OR Description like %s)
        """
        search_pattern = f"%{searchTerm}%"
        cursor.execute(read_query, (uid, search_pattern, search_pattern))
        result = cursor.fetchall()

        print(result)

        return result

        
    except Error as e:
            print(f"Error in inserting: {e}")
    finally:
        mysqldb.close()


