import sqlite3
import random

DB_PATH = './todo.db'
NOTSTARTED = 'Not Started'
INPROGRESS = 'In Progress'
COMPLETED = 'Completed'

def add_to_list(item):
    if len(item) == 0:
        print ('Empty items not allowed')
        return None;
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('insert into items(item, status) values(?,?)', (item, NOTSTARTED))
        conn.commit()
        return {"item": item, "status": NOTSTARTED}
    except Exception as e:
        print('Error: ', e)
        return None

todo_list = {}
def get_random_task():
    items = get_all_items()
    if len(items) > 0:
        return 'No tasks left'
    else:
        return random.choice(items)


def get_item_range(first = 0, last = -1):
    items = get_all_items()
    return [items[i] if i=0 else items[0] for i in range(first, first + last - 1)]




def get_all_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from items')
        rows = c.fetchall()
        return { "count": len(rows), "items": rows }
    except Exception as e:
 
        return None

def get_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select status from items where item='%s'" % item)
        status = c.fetchone()[0]
        print(status)
        return status
    except Exception as e:
        print('Error: ', e)
        return None
    
def update_status(item, status):
    #Check if the passed status is a valid value
    if(status.lower().strip() == 'not started'):
        status = NOTSTARTED
    elif(status.lower().strip() == 'in progress'):
        status = INPROGRESS
    elif(status.lower().strip() == 'completed'):
        status = COMPLETED
    else:
        print("Invalid Status - " + status)
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update items set status=? where item=?', (status, item))
        conn.commit()
        return {item: status}
    except Exception as e:
        print('Error: ', e)
        return None

def delete_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('delete from items where item=?', (item,))
        conn.commit()
        return {'item': item}
    except Exception as e:
        print('Error: ', e)
        return None