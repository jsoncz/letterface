import os, sys, time, random
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import argparse

#set up file agrument parsing
argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--i", required=True, help="Path to image.")
argumentParser.add_argument("--gif", required=False, type=int, help="GIF Mode: --g [number of frames]")
argumentParser.add_argument("--o", required=True, type=str, help="Output filename: --o CAT")
argumentParser.add_argument("--dur", required=False, type=int, help="Set duration for GIF Mode.")
argumentParser.add_argument("--r", required=False, type=str, help="Add a reverse to the GIF: --r Y")
argumentParser.add_argument("--f", required=False, type=str, help="Grow Font in Animation: --fg Y")
argumentParser.add_argument("--m", required=False, type=int, help="magic number for GIF: --m 13.")
argumentParser.add_argument("--x", required=False, type=int, help="Modulus for X.")
argumentParser.add_argument("--y", required=False, type=int, help="Modulus for Y.")
argumentParser.add_argument("--size", required=True,type=int, help="Font size.")
argumentParser.add_argument("--text", required=True, type=str, help="Text to use.")
argumentParser.add_argument("--printargs", required=False, help="Print Arguments to image")
arguments = vars(argumentParser.parse_args())
#setup default parameters

if arguments["x"] is None:
    xmod = 5
else:
    xmod = int(arguments["x"])
if arguments["y"] is None:
    ymod = 10
else:
    ymod = int(arguments["y"])
if arguments["dur"] is None:
    dur = 300
else:
    dur = int(arguments["dur"])
if arguments["r"] == 'Y':
    reverse = True;
else:
    reverse = False
if arguments["f"] == 'Y':
    fontgrow = True;
else:
    fontgrow = False

if arguments["m"] is None:
    magic = 13
else:
    magic = arguments["m"]
#load / open the image
image = Image.open(arguments["i"])
#convert to RGB for grabbing pixel data easier later
rgb_im = image.convert('RGB')
#fonts
#font = ImageFont.truetype("./monof555.ttf", fontsize)
argfont = ImageFont.truetype("./monof555.ttf", 11)
#couter for the Text string loop that comes later
count = 0
fontsize = arguments["size"]
#functions
def makeGif(frames):
    global xmod, ymod, fontsize
    images = []
    for i in range(frames):
        images.append(Image.new(mode = "RGB", size = (image.size[0], image.size[1])))
        images[i].convert('RGB')
        if fontgrow==True:
            if i > round(frames/3):
                fontsize+=i
        if reverse==True:
            if i <= (frames/2) % magic:
                if xmod<5:
                    xmod+=i/2
                if ymod<5:
                    ymod+=i/2
            else:
                xmod+=i
                ymod+=i

        #get pixel RGB information
        for j in range(image.size[0]):
            for k in range(image.size[1]):
                if k % (xmod)== 1:
                    if j % (ymod)== 1:
                        drawpixel(j,k, ImageDraw.Draw(images[i]),fontsize)
        #WATERMARK
        #ImageDraw.Draw(images[i]).text((10,250),"LetterFace",(255,255-i*4,255-i),ImageFont.truetype("./Sansation_Bold.ttf", 80))
        #ImageDraw.Draw(images[i]).text((100,350),"  by Jason B",(250,255,255-i),ImageFont.truetype("./monof555.ttf", 40))

        # save the images
        #maxsize = (800, 600)
        #images[i].thumbnail(maxsize, PIL.Image.ANTIALIAS)
        images[i].save('./output/'+str(i)+'.jpg')
    #after the loop for each frame processed, lets try to make the gif
    images[0].save('./GIFS/'+arguments["o"]+'.gif', format='GIF',
               append_images=images[1:],
               save_all=True,
               duration=dur, loop=0)


def drawpixel(i,j, imgdraw, fontsize):
    font = ImageFont.truetype("./monof555.ttf", fontsize)
    mystring = arguments["text"]
    global count
    if count==len(mystring)-1:
        count=0
    else:
        count+=1

    r, g, b = rgb_im.getpixel((i, j))
    #Amazing algo to print the string in a loop, Buddha - maybe I am stupid but this is the way I found
    imgdraw.text((i, j),mystring[count],(r,g,b),font=font)

# summarize some details about the image
print(image.format)
print(image.mode)
print(image.size)

#if no gif option is specified, we will just create one image based on the user settings
if arguments["gif"] is None:
    #create the image to draw text onto
    image1 = Image.new(mode = "RGB", size = (image.size[0], image.size[1]))
    draw = ImageDraw.Draw(image1)
    #get pixel RGB information
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if i % xmod == 1:
                if j % ymod == 1:
                    drawpixel(i,j, draw, arguments["size"])

    #check printargs mode
    if arguments["printargs"] == "Y":
        draw.text((1,1),str(arguments),(255,255,255),font=argfont)
        print (str(arguments))

    # show the image
    image1.show()
    image1.save('./output/' +time.strftime("%Y%m%d-%H%M%S")+'.jpg')

elif arguments["gif"] == 1:
    print ("Gif mode is for more than 1 frame...")
    sys.exit()

else:
    #if there is a gif param, parse the amount of frames specified to the function to make a gif
    makeGif(int(arguments["gif"]))
