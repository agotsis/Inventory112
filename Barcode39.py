# Barcode39.py
# Alexander Gotsis + agotsis + EE
# Creates Code 39 barcodes for use with scanners as ID tags. 
# Written from scratch

from tkinter import *
from PIL import Image, ImageDraw, ImageFont #classes used for the barcodes

class Barcode39(object):
    digitEncoding = { #this is the encoding scheme for a Code39 Barcode
    10: "100101101101", #represents start and stop digit, or *
    0: "101001101101",
    1: "110100101011",
    2: "101100101011",
    3: "110110010101",
    4: "101001101011",
    5: "110100110101",
    6: "101100110101",
    7: "101001011011",
    8: "110100101101",
    9: "101100101101",
    }

    font = ImageFont.truetype("bin/Microsoft Sans Serif.ttf", 16) #font for text

    def __init__(self, value, text = None, width=160, height=80):
        if isinstance(value, str):
            self.value = value
        else:
            self.value = str(value)
        self.height = height
        self.text = text
        self.labelHeight = self.height // 4 if self.text != None else 0
        self.width = width
        
        self.encoding = Barcode39.digitEncoding[10] + "0" #start digit
        for char in self.value:
            char = int(char)
            self.encoding += Barcode39.digitEncoding[char]
            self.encoding += "0" #intercharacter space
        self.encoding += Barcode39.digitEncoding[10] #end digit

    def tkDraw(self, x, y, canvas): #tkinter drawing function
        barWidth = self.width // len(self.encoding)
        for digitIndex in range(len(self.encoding)): #loop through, draw bars
            xVal = digitIndex * barWidth
            if self.encoding[digitIndex] == "1":
                for offset in range(barWidth):
                    canvas.create_line(xVal + offset, 0, xVal + offset, 
                        self.height, width = 1)

    def PILWrite(self, filename):
        barWidth = self.width // len(self.encoding)
        barcode = Image.new("RGB", (barWidth * len(self.encoding), 
            self.height + self.labelHeight), "white")
        draw = ImageDraw.Draw(barcode)
        for digitIndex in range(len(self.encoding)):
            xVal = digitIndex * barWidth
            for offset in range(barWidth):
                if self.encoding[digitIndex] == "1":#draw black rect if encoded
                    thisX = xVal + offset
                    draw.line((thisX, 0, thisX, self.height), 
                            fill="black", width = 1)
        if self.text != None:
            draw.text((0, self.height),self.text ,(0,0,0),
                font= Barcode39.font)
        try:
            barcode.save(filename) #write it to a file!
        except:
            raise IOError("That's an invalid filename!")

def draw(canvas, width, height): #call the tkinter drawing function
    code1.tkDraw(20, 20, canvas)

def runDrawing(width=300, height=300): 
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    draw(canvas, width, height)
    root.mainloop()
    print("bye!")

def test(): #test some sample barcodes
    code1 = Barcode39(1, text="1: L-Acoustics 115XT")
    code1.PILWrite("bin/code1.jpg") 
    Barcode39(2674, width= 350, height = 60).PILWrite("bin/code2.jpg")

if __name__ == "__main__":
    test()