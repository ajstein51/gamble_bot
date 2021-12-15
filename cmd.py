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


########################################################################################################
################################  MONEY COMMANDS  ######################################################
########################################################################################################


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
        # get cursor
        cur = dbcon.cursor()

        # see if he has that much in his hand
        cur.execute("""SELECT bankmoney, handmoney FROM gamble_db WHERE user = {0}""".format(username))
        checkamount = cur.fetchone()
    
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
    elif args[0] == 'all':
        cur = dbcon.cursor()
        
        # get the amounts
        cur.execute("""SELECT bankmoney, handmoney FROM gamble_db WHERE user = {0}""".format(username))
        checkamount = cur.fetchone()
        
        # if they have money in hand
        if checkamount[1] > 0:
            # swap all handmoney to bankmoney
            totalbank = checkamount[0] + checkamount[1]
            cur.execute("""UPDATE gamble_db SET bankmoney = {0}, handmoney = 0 WHERE user = {1}""".format(totalbank, username))
            
            # ret
            return totalbank
        else:
            return -1
    else:
        # not a number error out
        return -2    
# end of dep all
########################################################################################################
# withdraw function
def withdraw(username, args):
    # check the regex of the args
    numcheck = re.match('[0-9]+', args[0])
    
    if numcheck:
        # get cursor
        cur = dbcon.cursor()
        
        # check if they have that much in the bank
        cur.execute("""SELECT bankmoney, handmoney FROM gamble_db WHERE user = {0}""".format(username))
        checkamount = cur.fetchone()
        
        # if they do have that much and its <= how much they want
        if checkamount[0] is not None and checkamount[0] >= int(args[0]):
            # they did have that much in the bank so we convert it to hand money
            # get total of bank money
            totalbank = checkamount[0] - int(args[0])
            totalhand = checkamount[1] + int(args[0])
            # do the db query
            cur.execute("""UPDATE gamble_db SET bankmoney = {0}, handmoney = {1} WHERE user = {2}""".format(totalbank, totalhand, username))
            # save the transactoin
            dbcon.commit()
            return totalhand
        else:
            # they didnt have that much
            return -1
    elif args[0] == 'all':
        cur = dbcon.cursor()
        
        # get the amounts
        cur.execute("""SELECT bankmoney, handmoney FROM gamble_db WHERE user = {0}""".format(username))
        checkamount = cur.fetchone()
        
        # if they have anything in the bank
        if checkamount[0] > 0:
            # swap all bankmoney to handmoney
            totalhand = checkamount[0] + checkamount[1]
            cur.execute("""UPDATE gamble_db SET bankmoney = 0, handmoney = {0} WHERE user = {1}""".format(totalhand, username))
            
            # ret
            return totalhand
        else:
            return -1
    else:
        return -2
# end of withdraw
########################################################################################################
# get inventory
def inv(username):
    # get cursor
    cur = dbcon.cursor()
    
    # get their inventory
    cur.execute("""SELECT inventory FROM gamble_db WHERE user = {0}""".format(username))
    
    return cur.fetchone()
# end of get inv
########################################################################################################


########################################################################################################
################################  GET MONEY  ###########################################################
########################################################################################################


########################################################################################################
# work, give them a rank of money from 25 to 100
def work(username):
    # get random int
    rand_money = random.randint(25, 100)
    
    # get cur
    cur = dbcon.cursor()
    
    # put it in their handmoney
    cur.execute("""UPDATE gamble_db SET handmoney = {0} WHERE user = {1}""".format(rand_money, username))

    # save the transaction
    dbcon.commit()
    
    # return the amount
    return rand_money
# end of work
########################################################################################################
# fish
def fish(username):
    # Make the dictionary
    fishdic = {
        "goldfish" : 5,
        "blobfish" : 15,
        "tilapia" : 25,
        "shark" : 35,
        "snake" : 45,
        "alligator" : 55,
        "ring" : 500,
        "iphone" : 1000,
        "underwear" : 0,
        "sea-weed" : 0,
        "plastic bottle" : 0,
        "socks" : 0,
        "eel" : -5,
        "sting-ray" : -15,
        "bluefin tuna" : -50,
        "bomb" : -500,
    }
    
    # get random entry
    entries = list(fishdic.items())
    
    # get the pair
    rand_entry = random.choice(entries)
    
    # check if its worth anything
    if rand_entry[1] != 0:
        # get the cursor
        cur = dbcon.cursor()
        
        # get whats already in their inventory
        cur.execute("""SELECT inventory FROM gamble_db WHERE user = {0}""".format(username))
        getinv = cur.fetchone()
        print(getinv)
        # append on what they got
        wordlist = getinv[0] + ',' + rand_entry[0]
        print(wordlist)
        # put the item in their inv
        cur.execute("""UPDATE gamble_db SET inventory = '{0}' WHERE user = {1}""".format(wordlist, username))
        
        # commit
        dbcon.commit()
    # end of if
    
    
    return rand_entry
# end of fish
########################################################################################################
# high/low command
def highlow():
    # get user, query their on hand money, if its less than X amount error, else have them guess
    print('do later')
# end of highlow
########################################################################################################



# note
# use ctx.created_at for time stamp in UTC 