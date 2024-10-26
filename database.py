import sqlite3
from config import DB_PATH



def connect():
    db = sqlite3.connect(DB_PATH)
    return db



def create_tables():
    db = connect()
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userinf(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usertasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_name TEXT NOT NULL,
            status TEXT NOT NULL,
            creation_date DATETIME NOT NULL,
            last_update DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES userinf(user_id)
        )
    ''')

    db.commit()
    db.close()


# Add new user to userinf
def add_user(user_id):
    db = connect()
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO userinf (user_id) VALUES (?)", (user_id,))
    except sqlite3.IntegrityError:
        print(f"Registration failed, user with ID: {user_id} already exists")
    
    db.commit()
    db.close()


# Add new task to usertasks
def add_task(user_id, task_name, status, creation_time, last_update):
    db = connect()
    cursor = db.cursor()

    try: 
        cursor.execute("INSERT INTO usertasks (user_id, task_name, status, creation_date, last_update) VALUES (?, ?, ?, ?, ?)", (user_id, task_name, status, creation_time, last_update))
    except sqlite3.IntegrityError:
        print(f"ERROR, can't add task to user with ID: {user_id}")

    db.commit()
    db.close()


# Get all tasks created by user
def get_task_list(user_id):
    db = connect()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM usertasks WHERE user_id = ?", (user_id,))
    tasks = cursor.fetchall()

    db.close()
    return tasks


# Get one task by id
def get_task_by_id(task_id, user_id):
    db = connect()
    cursor = db.cursor()

    cursor.execute("SELECT task_name, status FROM usertasks WHERE user_id = ? AND id = ?", (user_id, task_id))
    task = cursor.fetchone()

    db.close()
    return task


# Delete task by id
def delete_task_by_id(task_id, user_id) -> bool:
    db = connect()
    cursor = db.cursor()

    cursor.execute("DELETE FROM usertasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    db.commit()

    deleted_rows = cursor.rowcount
    db.close()

    return deleted_rows > 0


# Edit task by id
def edit_task_by_id(task_id, user_id, new_status, update_time):
    db = connect()
    cursor = db.cursor()

    cursor.execute("UPDATE usertasks SET status = ?, last_update = ? WHERE id = ? AND user_id = ?", (new_status, update_time, task_id, user_id))
    db.commit()
    
    upd_rows = cursor.rowcount

    db.close

    return upd_rows > 0