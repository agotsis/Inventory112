# Inventory112.py
# Alexander Gotsis + agotsis + EE

from tkinter import *
from tkinter import font
from PIL import Image, ImageTk  #for importing  images, making barcodes
import tkinter.messagebox, tkinter.simpledialog, tkinter.filedialog #UI stuff
import tkinter.simpledialog #more for UI
import DatabaseTest # this is the databse class I wrote
import Barcode39 # this is my barcode class
import urllib.request, json #used to fetch andrewID's from service

# I wrote this file entirely myself. Represents bulk of work. Tkinter is mean.

class Inventory112(Tk):
    def __init__(self, parent):
        Tk.__init__(self,parent)

        #graphics settings
        self.cartHeight = 20
        self.cartWidth = 30
        self.boxBorder = 10
        self.initialBarcodes = "bin/"
        self.resizable(False, False)
        self.monoFont = font.Font(family="Monaco", size=12)
        self.IDWidth = 10

        self.debug = False #change this to true for debugging information
        self.logo = ImageTk.PhotoImage(Image.open("bin/abtechlogo.png"))
        #loads ABTech logo

        self.delInventory = "Delete Item from Inventory"
        self.removeCart = "Remove Selected Item"

        self.RFIDlength = 8
        self.db = DatabaseTest.DB("DemonstrationDB") #initiate DB connection
        self.popupOpen = False # initialize to None to avoid crashes
        self.createWidgets()
        self.cart = []

    def createWidgets(self):
        self.grid() #grid is one type of view manager for tkinter
        self.initializeSidebar()
        self.sidebarFrame.grid(column=0)
        self.initializeCart()
        self.cartFrame.grid(column = 1, row = 0)

    def initializeSidebar(self):

        self.sidebarFrame = Frame()

        self.logoLabel = Label(self.sidebarFrame, image = self.logo)
        self.logoLabel.grid(column=0, sticky = "WE")

        self.searchVariable = StringVar() #string variable for the search field
        self.searchEntry = Entry(self.sidebarFrame, 
            textvariable=self.searchVariable, bd = self.boxBorder)
        self.searchVariable.set(u"Search here. ID only.")
        self.searchEntry.bind("<FocusIn>",self.clearSearchEntry)
        self.searchEntry.bind("<FocusOut>",self.resetSearchEntry)
        self.searchEntry.bind("<Return>", self.searchEntryEnter)#search on enter
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
            "Show Inventory", self.delInventory, "Make Barcodes"]
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
        self.cartFrame = Frame(self)
        self.initializeCartList()
        self.cartListFrame.grid(column=1, row = 0)

    def initializeCartList(self):
        self.cartListFrame = Frame(self)

        self.initalizeItemEntry()

        self.cartScroller = Scrollbar(self.cartListFrame) #create scroller
        self.cartList = Listbox(self.cartListFrame,
            yscrollcommand = self.cartScroller.set, 
            height = self.cartHeight, width = self.cartWidth, 
            font= self.monoFont)
        self.cartList.bind("<<ListboxSelect>>", self.cartSelectionUpdate)
        self.itemEntry.pack(side = "top", fill="x")
        self.cartScroller.pack(side = "right", fill = "y")

        self.cartList.pack(side = "left", fill = "both")
        self.cartScroller.config(command = self.cartList.yview)

    def initalizeItemEntry(self):
        self.itemEntryVariable = StringVar()
        self.itemEntry = Entry(self.cartListFrame, 
            textvariable=self.itemEntryVariable, bd = self.boxBorder)
        self.itemEntryVariable.set(u"Scan item here.")

        self.itemEntry.bind("<FocusIn>",self.clearItemEntry)
        self.itemEntry.bind("<FocusOut>",self.resetItemEntry)
        self.itemEntry.bind("<Return>", self.itemEntryEnter)

    def popupListDo(self, winTitle):
        self.popupOpen = True
        self.popup = Toplevel(self)
        self.popup.title(winTitle)
        self.popup.protocol('WM_DELETE_WINDOW', self.deletePopup)
        popupScrollerFrame = Frame(self.popup)

        popupScroller = Scrollbar(popupScrollerFrame)
        self.popupList = Listbox(popupScrollerFrame,
            yscrollcommand = popupScroller.set, 
            height = self.cartHeight, width = self.cartWidth * 2, 
            font=self.monoFont)

        popupScroller.pack(side = "right", fill = "y")
        self.popupList.pack(side = "left", fill = "both")
        popupScroller.config(command = self.popupList.yview)
        
        ok = Button(self.popup, text="OK", command=self.deletePopup)
        popupScrollerFrame.grid(column = 0)
        ok.grid(column = 0, sticky = "WE")

        self.updatePopupList()

    def deletePopup(self):
        self.popupOpen = False
        self.popup.destroy()

    def updatePopupList(self):
        if not self.popupOpen:
            return
        fields = 3
        fieldWidth = self.cartWidth
        items = self.db.get("select id, name, location, checkedOut from items")
        self.popupList.delete(0, END)
        self.popupList.selection_clear(0,END)
        idIdx, nameIdx, locationIdx, checkedOutIdx = 0, 1, 2, 3
        for item in items:
            ID, name = item[idIdx], item[nameIdx]
            location, checkedOut = item[locationIdx], item[checkedOutIdx]
            if checkedOut != 0: locusInfo = self.convertToAndrewID(checkedOut)
            else: locusInfo = location
            displayThis = ""
            displayThis += str(ID) + " " * (self.IDWidth - len(str(ID)))
            displayThis += name + " " * (fieldWidth - len(name))
            displayThis += locusInfo + " " * (fieldWidth - len(locusInfo))
            if self.debug: print(displayThis)
            self.popupList.insert("end", displayThis)

    def highlightItemButtons(self):
        self.checkIn["highlightbackground"] = "red"
        self.checkOut["highlightbackground"] = "yellow"

    def dehighlightItemButtons(self):
        self.checkIn["highlightbackground"] = "white"
        self.checkOut["highlightbackground"] = "white"

    def switchToRemove(self):
        self.delete["text"] = self.removeCart
        self.delete["command"] = self.removeCartDo
        self.delete["highlightbackground"] = "yellow"

    def switchFromRemove(self):
        self.delete["text"] = self.delInventory
        self.delete["command"] = self.deleteDo
        self.delete["highlightbackground"] = "white"

    def itemEntryEnter(self, event):
        entry = self.itemEntryVariable.get()
        if not entry.isdigit():
            tkinter.messagebox.showwarning("Error!","Invalid entry!")
        else:
            item = self.db.get("""select id, name from\
                items where id = %s""" % entry)
            item = self.db.get("""select id, name, location, checkedOut from\
                items where id = %s""" % entry)
            if item == []: # database returned nothing
                tkinter.messagebox.showwarning(
                    "No item!", "There was no item found with that ID.")
            else:
                item = item[0] #unnest the tuple
                ID, name = item[0], item[1]
                if item in self.cart:
                    tkinter.messagebox.showwarning("Duplicate!", 
                        "This item is already in the cart!")
                else:
                    self.cart.append(item)
                    displayThis = str(ID) + " " * (self.IDWidth - len(str(ID)))
                    displayThis += name + " " * (self.cartWidth//2 - len(name))
                    self.cartList.insert("end", "%s" % displayThis)
        self.resetItemEntryFull()
        self.cartUpdate()

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
                item = item[0] #unnest the item!
                ID, name = item[idIdx], item[nameIdx]
                location, checkedOut = item[locationIdx], item[checkedOutIdx] 
                if checkedOut != 0:
                    andrewID = self.convertToAndrewID(checkedOut)
                    tkinter.messagebox.showinfo("Item Search",
            "%s, with ID: %d, is checked out by %s." % (name, ID, andrewID))
                else:
                    tkinter.messagebox.showinfo("Item Search",
                        "%s, with ID: %d, is at %s." % (name, ID, location))
            self.searchVariable.set(u"Search here. ID only.")

    def clearSearchEntry(self, event):
        self.searchEntry.focus_set()
        self.searchEntry.delete(0, END)

    def resetSearchEntry(self, event):
        self.searchVariable.set(u"Search here. ID only.")

    def clearItemEntry(self, event):
        self.itemEntry.focus_set()
        self.itemEntry.delete(0, END)

    def resetItemEntry(self, event):
        self.itemEntryVariable.set(u"Scan item here.")

    def resetItemEntryFull(self):
        self.itemEntryVariable.set(u"Scan item here.")
        self.itemEntry.focus_set()
        self.itemEntry.selection_range(0, END)

    def cartSelectionUpdate(self, event):
        if self.cartList.curselection() != tuple():
            self.switchToRemove()
        else:
            self.switchFromRemove()

    def cartUpdate(self):
        if self.cart == []:
            self.dehighlightItemButtons()
        else:
            self.highlightItemButtons()
            
    def convertToAndrewID(self, key):
        andrewID = self.db.get("""select andrewid from users where\
                            id = %d""" % key)
        return andrewID[0][0]
            
    def lookupAndrewID(self, RFIDid):
        RFIDid = RFIDid.upper()
        url = "http://merichar-dev.eberly.cmu.edu:81/cgi-bin/card-lookup3?\
card_id=%s" % RFIDid #this is the url to query
        try:
            response = urllib.request.urlopen(url) #fetch from cardservice port
        except urllib.error.HTTPError:
            tkinter.messagebox.showwarning("AndrewID Lookup Fails",
                    "Check the IP allow list. Are you allowed to access?")
            return
        data = json.loads(response.read().decode('utf-8')) #convert to string
        if self.debug: print(data)
        return data["andrewid"] #dictionary lookup in the JSON object!

    def addUserDo(self):
        user = tkinter.simpledialog.askstring("What user?", "andrewID to add?")
        if user == None:
            return #canceled, return
        if len(user) == self.RFIDlength: #only lookup if is correct length
            lookup = self.lookupAndrewID(user)
            if lookup != None:
                user = lookup
        lookup = self.db.get("""select id, andrewID, name from users where \
andrewID = '%s'""" % user)
        if lookup != []:
            tkinter.messagebox.showinfo("User Exists!!",
                    "The user %s already exists!" % user)
            return
        self.db.addUser(user)
        tkinter.messagebox.showinfo("User Success!",
                    "The user %s was created!" % user)

    def deleteDo(self):
        ID = tkinter.simpledialog.askinteger("Delete what?", 
            "Enter an ID to delete.")
        if ID == None:
            return #canceled, return
        item = self.db.get("""select id, name, location, checkedOut from\
                items where id = %s""" % ID)
        if item == []:
            tkinter.messagebox.showwarning(
                "No item!",
                "There was no item found with that ID.")
        else:
            self.db.delete(ID)
            self.updatePopupList()

    def makeBarcodesDo(self):
        location = tkinter.filedialog.askdirectory(
            initialdir= self.initialBarcodes, 
            title="Where do you want the Barcodes?")
        if location == None or len(location) <= 1: #nothing selected
            return
        else:
            items = self.db.get("select id, name, location from items")
        for item in items:
            (ID, name) = (item[0],item[1])  # 0 is ID index, 1 is name index
            barcode = Barcode39.Barcode39(ID, text = "%d: %s" % (ID, name))
            filename = "%s_%s.jpg" % (ID, name)
            try:
                barcodeHere = "%s/%s" % (location, filename)
                barcode.PILWrite(barcodeHere)
            except IOError:
                tkinter.messagebox.showwarning("Invalid Filename!",
                    "That filename is invalid!")
                return
        tkinter.messagebox.showinfo("Barcode Success!",
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
                    "Empty Cart!", "Cart is empty! Nothing to checkOut!")
            return
        user = tkinter.simpledialog.askstring("Check out to whom?", "andrewID?")
        if user == None: return #cancel was hit
        if len(user) == self.RFIDlength: #only try lookup if is correct length
            lookup = self.lookupAndrewID(user)
            if lookup != None: user = lookup
        item = self.db.get("""select id, andrewID, name from users where \
andrewID = '%s'""" % user)
        if item == []: #nobody found
            tkinter.messagebox.showwarning("No user!",
                "No user exists with that ID. You may try to add them.")
            return
        else:
            userID = item[0][0] #unnest the tuple, then first item
            for cartItem in self.cart:
                ID = cartItem[0] # 0 is ID index
                self.db.update("update items set checkedOut = %d where \
id = %d" % (userID, ID))
        self.resetCart()
        tkinter.messagebox.showinfo("CheckOut Success!",
                    "All items successfully checked out to %s!" % user)

    def removeCartDo(self):
        selection = self.cartList.curselection()
        cartItem = self.cartList.get(selection)
        removeID = int(cartItem.split(" ")[0])
        for item in self.cart:
            if item[0] == removeID:
                self.cart.remove(item)
                break
        self.cartList.delete(selection)
        if self.debug: print(self.cart)
        self.cartList.selection_clear(0,END)
        self.cartSelectionUpdate(None)
        self.cartUpdate()

    def resetCart(self):
        self.resetItemEntryFull()
        self.cart = []
        self.cartList.delete(0, END)
        self.cartList.selection_clear(0,END)
        self.cartSelectionUpdate(None)
        self.cartUpdate()
        self.updatePopupList()

    def addItemDo(self):
        name = tkinter.simpledialog.askstring("Item name?", 
            "What is the item name?")
        if name == None:
            return #canceled, return
        elif name == "":
            tkinter.messagebox.showwarning("No name!", 
                "You need to supply a name!")
            return
        location = tkinter.simpledialog.askstring("Item location?", 
            "Where is the item?")
        if location == None:
            return #canceled, return
        elif location == "":
            tkinter.messagebox.showwarning("No location!", 
                "You need to supply a location!")
            return
        self.db.addToDB(name, location, 0) #defaults checked in
        self.updatePopupList()

    def listDo(self):
        if not self.popupOpen:
            self.popupListDo("Inventory View")

if __name__ == "__main__":
    app = Inventory112(None)
    app.title("ABTech Inventory 112")
    app.mainloop()
    print("Quitting!")