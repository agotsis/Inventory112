# demo1.py
# Alex Gotsis + agotsis + EE + 3-8-16

#original code. Most basic image learning.

from PIL import Image, ImageFilter

try:
    original = Image.open("bin/Lenna.png")
except:
    print("Unable to load image")

print("The size of the Image is: ")
print(original.format, original.size, original.mode)