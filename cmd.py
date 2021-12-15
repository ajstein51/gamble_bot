# includes
import sqlite3
from sqlite3 import Error
import random
import os.path
import re

########################################################################################################
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
########################################################################################################
# get bal
def get_bal(username):
   cur = dbcon.cursor()
   
   # get the balance
   cur.execute("""SELECT bankmoney, handmoney FROM gamble_db WHERE user = {0}""".format(username))
   ret = cur.fetchone()
   return ret
        
# end of bal function
########################################################################################################
# dep all
def deposit(username, args):
    # check the regex
    numcheck = re.match("[0-9]+", args[0])
    
    if numcheck:
        # its a number got a number
        
        # get cursor
        cur = dbcon.cursor()

        # see if he has that much in his hand
        cur.execute("""SELECT bankmoney, handmoney FROM gamble_db WHERE user = {0}""".format(username))
        checkamount = cur.fetchone()
        print(checkamount, args[0])
        # first if is an edge case of hes not in db and doesn't have money
        if checkamount is not None:
            # checkamount is a tuple thus we need the first element
            if int(args[0]) <= checkamount[1]:
                # get total of deposit and whats in his bank
                total_amount = checkamount[0] + int(args[0])
                sub_amount = checkamount[1] - int(args[0])
                cur.execute("""UPDATE gamble_db SET bankmoney = {0}, handmoney = {1} WHERE user = {2}""".format(total_amount, sub_amount, username))
                dbcon.commit()
                return args[0]
            else:
                # doesnt have that much
                return -1
        else:
            return -1
    else:
        # not a number error out
        return -2    
# end of dep all
########################################################################################################

########################################################################################################

########################################################################################################
# high/low command
def highlow():
    # get user, query their on hand money, if its less than X amount error, else have them guess
    print('do later')
# end of highlow
########################################################################################################
