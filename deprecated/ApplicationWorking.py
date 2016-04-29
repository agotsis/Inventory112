# ApplicationWorking.py
# Alexander Gotsis + agotsis + EE

from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox, tkinter.simpledialog, tkinter.filedialog
import tkinter.simpledialog
import DatabaseTest
import Barcode39
import os

# I wrote this file entirely myself.

class Inventory112(Tk):
    def __init__(self, parent):
        Tk.__init__(self,parent)

        #graphics settings
        self.cartHeight = 20
        self.cartWidth = 30
        self.initialBarcodes = "bin/Barcodes"
        self.resizable(False,False)
        #self["background"] = "red" # for debugging

        self.logo = photo = ImageTk.PhotoImage(Image.open("bin/abtechlogo.png"))
        #loads logo

        self.parent = parent
        self.db = DatabaseTest.DB("TestDB")
        self.createWidgets()
        self.cart = []

    def createWidgets(self):
        self.grid()
        self.initializeSidebar()
        self.sidebarFrame.grid(column=0)
        self.initializeCart()
        self.cartFrame.grid(column = 1, row = 0)
        #self.grid_columnconfigure(1,weight=1)

    def initializeSidebar(self):

        self.sidebarFrame = Frame()

        self.logoLabel = Label(self.sidebarFrame, image = self.logo)
        self.logoLabel.grid(column=0, sticky = "WE")

        self.searchVariable = StringVar()
        self.searchEntry = Entry(self.sidebarFrame, 
            textvariable=self.searchVariable)
        self.searchVariable.set(u"Search here. ID only.")
        self.searchEntry.bind("<Return>", self.searchEntryEnter)
        self.searchEntry.grid(column=0, sticky = "WE")
        #search initialization
        
        #create all the buttons!
        self.initializeButtons()
        

    def initializeButtons(self):
        self.addItem = Button(self.sidebarFrame)
        self.addUser = Button(self.sidebarFrame)
        self.search = Button(self.sidebarFrame)
        self.addBin = Button(self.sidebarFrame)
        self.makeBarcodes = Button(self.sidebarFrame)
        self.checkIn = Button(self.sidebarFrame)
        self.checkOut = Button(self.sidebarFrame)
        self.delete = Button(self.sidebarFrame)

        nameList = ["Check In", "Check Out", "Add Item", "Add User", 
            "List Items", "Delete Item", "Make Barcodes"]
        buttonList = [self.checkIn, self.checkOut,  self.addItem, self.addUser,
            self.search, self.delete, self.makeBarcodes]
        action = [self.checkInDo, self.checkOutDo, self.addItemDo,
            self.addUserDo, self.listDo, self.deleteDo, self.makeBarcodesDo]

        for index in range(len(buttonList)):
            buttonRef = buttonList[index]
            buttonRef["text"] = nameList[index]
            buttonRef["command"] = action[index]
            buttonRef.grid(column=0, sticky = "WE")

    def initializeCart(self):
        self.cartFrame = Frame(self, background ="red")
        # self.bottomFrame = Frame(self.cartFrame)

        # self.checkIn = Button(self.cartFrame)
        # self.checkOut = Button(self.cartFrame)
        

        self.initializeCartList()

        self.cartListFrame.grid(column=1, row = 0)

    def initializeCartList(self):
        self.cartListFrame = Frame(self)

        self.itemEntryVariable = StringVar()
        self.itemEntry = Entry(self.cartListFrame, 
            textvariable=self.itemEntryVariable)
        self.itemEntryVariable.set(u"Scan item here.")
        self.itemEntry.focus_set()
        self.itemEntry.selection_range(0, END)

        self.itemEntry.bind("<Return>", self.itemEntryEnter)

        self.cartScroller = Scrollbar(self.cartListFrame)
        self.cartList = Listbox(self.cartListFrame,
            yscrollcommand = self.cartScroller.set, 
            height = self.cartHeight, width = self.cartWidth)
        self.itemEntry.pack(side = "top", fill="x")
        self.cartScroller.pack(side = "right", fill = "y")

        # for line in range(150):
        #     self.cartList.insert("end", "This is line number " + str(line))

        self.cartList.pack(side = "left", fill = "both")
        self.cartScroller.config(command = self.cartList.yview)

    def itemEntryEnter(self, event):
        entry = self.itemEntryVariable.get()
        print(repr(entry))
        if not entry.isdigit():
            tkinter.messagebox.showwarning(
                "Error!",
                "Invalid entry!")
        else:
            item = self.db.get("""select id, name, location, checkedOut from\
                items where id = %s""" % entry)
            if item == []:
                tkinter.messagebox.showwarning(
                    "No item!",
                    "There was no item found with that ID.")
            else:
                item = item[0]
                if item in self.cart:
                    tkinter.messagebox.showwarning(
                    "Duplicate!",
                    "This item is already in the cart!")
                else:
                    self.cart.append(item)
                    displayThis = "%-15d %15s" % (item[0], item[1]) #width/2
                    self.cartList.insert("end", "%s" % displayThis)
        self.itemEntryVariable.set(u"Scan item here.")
        self.itemEntry.focus_set()
        self.itemEntry.selection_range(0, END)

    def searchEntryEnter(self, event):
        entry = self.searchVariable.get()
        if not entry.isdigit():
            tkinter.messagebox.showwarning("Error!","Invalid entry!")
        else:
            item = self.db.get("""select id, name, location, checkedOut from\
                items where id = %s""" % entry)
            if item == []:
                tkinter.messagebox.showwarning(
                    "No item!", "There was no item found with that ID.")
            else:
                idIdx, nameIdx, locationIdx, checkedOutIdx = 0, 1, 2, 3
                item = item[0]
                ID = item[idIdx] # 0 is ID index
                name = item[nameIdx] # 1 is name index
                location = item[locationIdx] # 1 is name index
                checkedOut = item[checkedOutIdx] # 3 is name index
                if checkedOut != 0:
                    andrewID = self.db.get("""select andrewid from users where\
                            id = %d""" % checkedOut)
                    print(andrewID)
                    andrewID = andrewID[0][0]
                    print(andrewID)
                    tkinter.messagebox.showinfo(
                        "Item Search",
                        "%s, with ID: %d, is checked out \
by %s." % (name, ID, andrewID))
                else:
                    tkinter.messagebox.showinfo(
                        "Item Search",
                        "%s, with ID: %d, is at %s." % (name, ID, location))
            self.searchVariable.set(u"Search here. ID only.")

    def selectEntry(self):
        self.itemEntry.selection_range(0, END)

    def addUserDo(self):
        user = tkinter.simpledialog.askstring("What user?", 
            "andrewID to add?")
        self.db.addUser(user)

    def deleteDo(self):
        ID = tkinter.simpledialog.askinteger("Delete what?", 
            "Enter an ID to delete.")
        item = self.db.get("""select id, name, location, checkedOut from\
                items where id = %s""" % ID)
        if item == []:
            tkinter.messagebox.showwarning(
                "No item!",
                "There was no item found with that ID.")
        else:
            self.db.delete(ID)

    def makeBarcodesDo(self):
        location = tkinter.filedialog.askdirectory(
            initialdir= self.initialBarcodes, 
            title="Where do you want the Barcodes?")
        if location == None or len(location) <= 1: #nothing selected
            return
        else:
            items = self.db.get("select id, name, location from items")
        for item in items:
            ID = item[0] # 0 is ID index
            name = item[1] # 1 is name index
            barcode = Barcode39.Barcode39(ID)
            filename = "%s_%s.jpg" % (ID, name)
            try:
                barcodeHere = "%s/%s" % (location, filename)
                barcode.PILWrite(barcodeHere)
            except IOError:
                tkinter.messagebox.showwarning(
                    "Invalid Filename!",
                    "That filename is invalid!")
                return
        tkinter.messagebox.showinfo(
                    "Barcode Success!",
                    "Barcodes were successfully created in %s!" % location)

    def checkInDo(self):
        if self.cart == []: #cart is empty
            tkinter.messagebox.showwarning(
                    "Empty Cart!",
                    "Cart is empty! Nothing to checkIn!")
            return
        for item in self.cart:
            ID = item[0] # 0 is ID index
            command ="update items set checkedOut = 0 where id = %d" % ID
            self.db.update(command)
        self.resetCart()
        tkinter.messagebox.showinfo(
                    "CheckIn Success!",
                    "All checked out items were checked in!")

    def checkOutDo(self):
        if self.cart == []: #cart is empty
            tkinter.messagebox.showwarning(
                    "Empty Cart!",
                    "Cart is empty! Nothing to checkOut!")
            return
        user = tkinter.simpledialog.askstring("Check out to whom?", 
            "andrewID?")
        print(user)
        item = self.db.get("""select id, andrewID, name from users where\
 andrewID = '%s'""" % user)
        if item == []:
            tkinter.messagebox.showwarning(
                "No user!",
                "No user exists with that ID. You may try to create them.")
            return
        else:
            item = item[0]
            userID = item[0]
            for cartItem in self.cart:
                ID = cartItem[0] # 0 is ID index
                command ="update items set checkedOut = %d where\
                 id = %d" % (userID, ID)
                self.db.update(command)
        self.resetCart()
        tkinter.messagebox.showinfo(
                    "CheckOut Success!",
                    "All items successfully checked out to %s!" % user)

    def resetCart(self):
        self.itemEntryVariable.set(u"Scan item here.")
        self.itemEntry.focus_set()
        self.itemEntry.selection_range(0, END)
        self.cart = []
        self.cartList.delete(0, END)

    def addItemDo(self):
        name = tkinter.simpledialog.askstring("Item name?", 
            "What is the item name?")
        location = tkinter.simpledialog.askstring("Item location?", 
            "Where is the item?")
        #adder = AddDialog(self.parent)
        self.db.addToDB(name, location, 0) #defaults checked in

    def listDo(self):
        items = self.db.get("select id, name, location, checkedOut from items")
        for item in items:
            print(item)
        print("Items Listed")

    def addBinDo(self):
        print("Time to add a bin!")

if __name__ == "__main__":
    app = Inventory112(None)
    app.title("ABTech Inventory 112")
    app.mainloop()