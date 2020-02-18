import time
import random
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import argparse

#set up file agrument parsing
argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--i", required=True, help="Path to image.")
argumentParser.add_argument("--x", required=True, help="Modulus for X.")
argumentParser.add_argument("--y", required=True, help="Modulus for Y.")
argumentParser.add_argument("--size", required=False, help="Font size.")
argumentParser.add_argument("--text", required=True, help="Text to use.")
argumentParser.add_argument("--printargs", required=False, help="Print Arguments to image")

arguments = vars(argumentParser.parse_args())

if arguments["size"] is None:
    fontsize = 10
else:
    fontsize = int(arguments["size"])

#load / open the image
image = Image.open(arguments["i"])
image.resize((100, 160))
image1 = Image.new(mode = "RGB", size = (image.size[0], image.size[1]))
# summarize some details about the image
print(image.format)
print(image.mode)
print(image.size)
#convert to RGB for grabbing pixel data easier later
rgb_im = image.convert('RGB')

draw = ImageDraw.Draw(image1)
font = ImageFont.truetype("./monof55.ttf", fontsize)
argfont = ImageFont.truetype("./monof55.ttf", 11)

#get pixel RGB information
def getpixel(i,j):
    mystring = arguments["text"]
    r, g, b = rgb_im.getpixel((i, j))
    draw.text((i, j),mystring[random.randint(0,len(mystring)-1)],(r,g,b),font=font)
    print (mystring[random.randint(0,len(mystring)-1)], end="", flush=True)

for i in range(image.size[0]):
    for j in range(image.size[1]):
        #COOL Pattern with Triangle
        # if i % int(arguments["x"]) & j % int(arguments["y"]) == 1:
        #     getpixel(i,j)
        # else:
            #     image1.putpixel((i,j), (0,0,0))
        if i % int(arguments["x"]) == 1:
            if j % int(arguments["y"]) == 1:
                getpixel(i,j)
        #else:
            #image1.putpixel((i,j), (0,0,0))
#check printargs mode
if arguments["printargs"] == "Y":
    draw.text((1,1),str(arguments),(255,255,255),font=argfont)
    print (str(arguments))

# show the image
image1.show()
image1.save(time.strftime("%Y%m%d-%H%M%S")+'.jpg')
