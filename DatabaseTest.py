# DatabaseTest.py
# Alexander Gotsis + agotsis + EE

# This is original code. Demonstrating understanding of databases.

import sqlite3

class DB(object):
    def __init__(self, name):
        self.db = sqlite3.connect('data/%s' % name) #create/connect to database
        self.cursor = self.db.cursor() #everything with database uses cursor
        self.db.commit() #MUST commit changes! to db

        self.debug = False #set to True to print debugging info

    def createTable(self, name): #overwrites tables!
        self.cursor.execute("DROP TABLE IF EXISTS %s" % name) #remove if exists
        self.cursor.execute('''
            CREATE TABLE %s(id INTEGER PRIMARY KEY, name TEXT, 
            location TEXT,
            checkedOut, INTEGER)''' % name) #All sqlite functions use execute

    def createUsers(self):
        self.cursor.execute("DROP TABLE IF EXISTS %s" % "users")#remove existing
        self.cursor.execute('''
            CREATE TABLE %s(id integer PRIMARY KEY, andrewid TEXT, name TEXT)
            ''' % "users") #All sqlite functions use execute


    def addToDB(self, name, location, checkedOut): 
        #to be imporoved with *args so that anything can be added
        self.cursor.execute('''INSERT INTO items(name, location, checkedOut)
                  VALUES(?,?,?)''', (name, location, checkedOut))
        try:
            self.db.commit()
        except:
            print("insert failed!")
        if self.debug:
            print("insert successful!")

    def addUser(self, andID):
        self.cursor.execute('''INSERT INTO users(name, andrewid)
                  VALUES(?,?)''', ("",andID))
        try:
            self.db.commit() #makes the actual changes to database
        except:
            print("insert failed!")
        if self.debug:
            print("insert successful!")

    def get(self, command):
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def update(self, command):
        self.cursor.execute(command)
        try:
            self.db.commit()
        except:
            print("update failed!")
        if self.debug:
            print("update successful!")

    def delete(self, ID):
        self.cursor.execute('''DELETE FROM items WHERE id = ? ''', (ID,))
        try:
            self.db.commit()
        except:
            print("delete failed!")
        if self.debug:
            print("delete successful!")

if __name__ == "__main__":
    db = DB("DemonstrationDB")

    # db.createTable("items") #uncomment to clear and recreate items table
    # db.createUsers()
    # db.addUser("agotsis")
    # db.addUser("kdodhia")

    #some test items to begin with
    # db.addToDB("Quadbox", "Tech 1", True)
    # db.addToDB("Quadbox", "Tech 1", False)
    # db.addToDB("Quadbox", "Tech 2", True)
    # db.addToDB("SOCA Case", "Tech 2", False)
    # db.addToDB("GrandMA 2", "Tech 1", False)

    print(db.get("""
        select id, name, location from items 
        where location = "Tech 1"
        """))
    print(db.get("""
        select id, andrewid, name from users"""))