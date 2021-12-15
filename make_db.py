# files to make the db 1 time

# includes
import sqlite3
from sqlite3 import Error
import random
import os.path

# get connection to db
def start_db():
    global dbcon
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        dbpath = os.path.join(BASE_DIR, 'gamble_db.db')
        dbcon = sqlite3.connect(dbpath)
    except Error as e:
        print(e)
# end of function

def make_db():
    if dbcon is not None:
        dbcon.execute("""CREATE TABLE IF NOT EXISTS gamble_db (user int, bankmoney int, handmoney int)""")
    else:
        print("error in dbcon")
# end of func

def main():
    start_db()
    make_db()
# end of func

# init main
if __name__ == '__main__':
    main()
    