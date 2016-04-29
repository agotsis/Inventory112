# ApplicationClassed.py

#Redundant file. Used for learning.

import tkinter as tk

class HomeScreen(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.createWidgets()

    def createWidgets(self):
        self.grid
        self.initializeSidebar()
        self.sidebarFrame.grid(column=0)
        self.initializeCart()
        self.cartFrame.grid(column = 1, row = 0)
        #self.grid_columnconfigure(1,weight=1)

    def initializeSidebar(self):
        self.sidebarFrame = tk.Frame(self)
        self.addItem = tk.Button(self.sidebarFrame)
        self.search = tk.Button(self.sidebarFrame)
        self.settings = tk.Button(self.sidebarFrame)
        self.addBin = tk.Button(self.sidebarFrame)
        self.quit = tk.Button(self.sidebarFrame)

        nameList = ["Add Item", "Search", "Add Bin", "Settings", "Quit"]
        buttonList = [self.addItem, self.search, self.settings, self.addBin,
            self.quit]
        action = [self.addItemDo, self.searchDo, self.addBinDo, self.settingsDo,
            self.destroy]

        for index in range(len(buttonList)):
            buttonRef = buttonList[index]
            buttonRef["text"] = nameList[index]
            buttonRef["command"] = action[index]
            buttonRef.grid(row=index, column=0, sticky = "WE")

    def initializeCart(self):
        self.cartFrame = tk.Frame(self)
        #self.bottomFrame = tk.Frame(self.cartFrame)

        self.checkIn = tk.Button(self.cartFrame)
        self.checkOut = tk.Button(self.cartFrame)

        nameList = ["Check In", "Check Out"]
        buttonList = [self.checkIn, self.checkOut]
        action = [self.checkInDo, self.checkOutDo]

        for index in range(len(buttonList)):
            buttonRef = buttonList[index]
            buttonRef["text"] = nameList[index]
            buttonRef["command"] = action[index]

        #self.bottomFrame.grid(side = "bottom")

        self.initializeCartList()

        #self.grid_columnconfigure(0,weight=1)

    def initializeCartList(self):
        self.cartListFrame = tk.Frame(self)
        self.itemEntry = tk.Entry(self.cartListFrame)
        self.cartScroller = tk.Scrollbar(self.cartListFrame)
        self.cartList = tk.Listbox(self.cartListFrame,
            yscrollcommand = self.cartScroller.set)
        self.itemEntry.pack(side = "top", fill="x")
        self.cartScroller.pack(side = "right", fill = "y")

        for line in range(11):
            self.cartList.insert("end", "This is line number " + str(line))

        self.cartList.pack(side = "left", fill = "both")
        self.cartScroller.config(command = self.cartList.yview)

    def checkOutDo(self):
        print("Time to checkOut")

    def checkInDo(self):
        print("Time to checkIn")

    def addItemDo(self):
        print("Time to add an item!")

    def searchDo(self):
        print("Time to search")

    def settingsDo(self):
        print("change settings!")

    def addBinDo(self):
        print("Time to add a bin!")
    def donothing(self):
       filewin = tk.Toplevel(self)
       button = Button(filewin, text="Do nothing button")
       button.pack()

       # self.cart.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = HomeScreen(None)
    app.title("Inventory 112")
    app.mainloop()