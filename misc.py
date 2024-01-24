from sqlite3 import connect

db = connect('database.db', check_same_thread=False)  #