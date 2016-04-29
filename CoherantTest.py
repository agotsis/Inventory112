# CoherantTest.py
# Alexander Gotsis + agotsis + EE

# a coherent text based test. Also serves as database wrapper
 
import Barcode39
import DatabaseTest

def runTest():
    db = DatabaseTest.DB("TestDB")
    #db.createTable("items") #Comment/uncomment this line to clear items table.

    def addItem():
        nonlocal db
        name = input("What item?\n")
        location = input("Where is it?\n")
        db.addToDB(name, location, False) # default is checked out

    def listItems():
        nonlocal db
        items = db.get("select id, name, location, checkedOut from items")
        for item in items:
            print(item)

    def makeBarcodes():
        nonlocal db
        items = db.get("select id, name, location, checkedOut from items")
        for item in items:
            ID = item[0] # 0 is ID index
            name = item[1] # 1 is name index
            barcode = Barcode39.Barcode39(ID)
            filename = "%s_%s.jpg" % (ID, name)
            barcode.PILWrite("bin/CoherantTest/%s" % filename)
            print("Barcode %s created in /bin/CoherantTest folder!" % filename)

    def lookupItem(ID):
        item = db.get("""select id, name, location, checkedOut from items where\
            id = %d""" % ID)
        if item == []:
            item = "No item found!"
            return
        print(item)
        if item[0][3]: # 3 is checkedOut index
            answer = input("Want to check in? (y/n)\n")
        else:
            answer = input("Want to check out? (y/n)\n")
        if answer == "y":
            flipCheckedOut(ID, item[0][3])

    def flipCheckedOut(ID, value):
        value = 0 if value == 1 else 1
        command ="update items set checkedOut = %d where id = %d" % (value, ID)
        db.update(command)


    def checkedOut():
        items=db.get("""select id, name, location, checkedOut from items where\
            checkedOut != 0""")
        if items == []:
            item = "No items checked out!"
        else:
            for item in items:
                print(item)

    def delete():
        ID = input("ID to delete?\n")
        db.delete(ID)

    while True:
        answer = input("""Enter Option or Scan Item:\n(A)dd Item\n(L)ist Items
(C)hecked Out\nMake (B)arcodes\n(U)ser Add\n(D)elete\n""")
        answer = answer.upper()
        if answer.isdigit():
            lookupItem(int(answer))
        elif answer == "A":
            addItem()
        elif answer == "L":
            listItems()
        elif answer == "B":
            makeBarcodes()
        elif answer == "C":
            checkedOut()
        elif answer == "D":
            delete()
        elif answer == "U":
            delete()
        else:
            print("Invalid input!")

runTest()