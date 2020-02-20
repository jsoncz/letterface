import os, sys, time, random
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

#couter for the Text string loop that comes later
count = 0

#final GIF Path (global variable)
gifpath=''

#functions
def makeGif(image, frames, dur, xmod, ymod, reverse, magic, fontsize, fontgrow, mystring, shrink):
    global gifpath
    print("frames, dur, xmod, ymod, reverse, magic, fontsize, fontgrow, mystring, shrink")
    print(frames, dur, xmod, ymod, reverse, magic, fontsize, fontgrow, mystring, shrink)

    #convert to RGB for grabbing pixel data easier later
    rgb_im = image.convert('RGB')
    images = []
    for i in range(frames):
        images.append(Image.new(mode = "RGB", size = (image.size[0], image.size[1])))
        images[i].convert('RGB')
        if fontgrow==True:
            if i > frames/2:
                fontsize+=round(magic*(i/3))
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
                if j % (xmod)== 1:
                    if k % (ymod)== 1:
                        drawpixel(image, j,k, ImageDraw.Draw(images[i]),fontsize, mystring)
        #WATERMARK
        #ImageDraw.Draw(images[i]).text((10,250),"LetterFace",(255,255-i*4,255-i),ImageFont.truetype("./Sansation_Bold.ttf", 80))
        #ImageDraw.Draw(images[i]).text((100,350),"  by Jason B",(250,255,255-i),ImageFont.truetype("./monof555.ttf", 40))

        # save the images
        maxsize = (round(image.size[0]/2), round(image.size[1]/2))
        if shrink==True:
            images[i].thumbnail(maxsize)
        images[i].save('./output/'+str(i)+'.jpg')
    #after the loop for each frame processed, lets try to make the gif
    gifpath='./GIFS/'+time.strftime("%Y%m%d-%H%M%S")+'.gif'

    images[0].save(gifpath, format='GIF',
               append_images=images[1:],
               save_all=True,
               duration=dur, loop=0)


def drawpixel(image, i,j, imgdraw, fontsize, mystring):
    font = ImageFont.truetype("./monof555.ttf", fontsize)
    global count
    if count==len(mystring)-1:
        count=0
    else:
        count+=1
    #convert to RGB for grabbing pixel data easier later
    rgb_im = image.convert('RGB')
    r, g, b = rgb_im.getpixel((i, j))
    #Amazing algo to print the string in a loop, Buddha - maybe I am stupid but this is the way I found
    imgdraw.text((i, j),mystring[count],(r,g,b),font=font)

from appJar import gui
app = gui()
app.setSize("640x600")
app.setTitle('LetterFace 0.1')
app.addLabel("title", "Welcome to LetterFace!")
app.setLabelBg("title", "orange")
app.addLabel("loaded")
app.addImage("animated", "logo.gif")
app.setFont(size=10, family="Verdana", underline=False)

def open(btn):
    global image
    file=app.openBox(title="Choose an Image", dirName=None, fileTypes=[('images', '*.png'), ('images', '*.jpg')], asFile=False, parent=None, multiple=False, mode='r')
    #load / open the image
    image = Image.open(file)
    app.setLabel("loaded", file+" Image Loaded")
    app.setLabelBg("loaded", "blue")

def doGif(btn):
    global gifpath
    frames=app.getScale("Animation Frames")
    dur=app.getScale("Animation Duration")
    mystring=app.getEntry("Text String")
    x=app.getScale("X")
    y=app.getScale("Y")
    magic=app.getScale("M")
    reverse=app.getCheckBox("Alt Flow")
    fontsize=app.getScale("Font Size")
    fontgrow=app.getCheckBox("Grow Font")
    shrink=app.getCheckBox("Shrink GIF")

    if mystring != "":
        app.setLabel("loaded", "...Processing")
        app.setLabelBg("loaded", "blue")
        makeGif(image, frames, dur, x, y,reverse, magic, fontsize, fontgrow, mystring, shrink)
        tmp=time.strftime("%Y%m%d-%H%M%S")
        app.startSubWindow(gifpath, modal=True)
        app.setBg("black", override=False, tint=False)
        app.addImage(tmp, gifpath)
        app.stopSubWindow()
        app.showSubWindow(gifpath)
    else:
        app.setLabel("loaded", " TEXT STRING MISSING!")
        app.setLabelBg("loaded", "red")

def start():
    app.addButton("Load Image to Edit", open)
    app.addLabelScale("Animation Frames")
    app.setScaleRange("Animation Frames", 1,50, curr=15)
    app.addLabelScale("Animation Duration")
    app.setScaleRange("Animation Duration", 20,250, curr=40)
    app.addLabelEntry("Text String")
    app.addCheckBox("Grow Font")
    app.addCheckBox("Alt Flow")
    app.addCheckBox("Shrink GIF")
    app.addLabel("options", "Modifiers")
    app.setLabelBg("options", "orange")
    app.addLabelScale("Font Size")
    app.setScaleRange("Font Size", 5,60, curr=15)
    app.addLabelScale("X")
    app.setScaleRange("X", 5,50, curr=24)
    app.addLabelScale("Y")
    app.setScaleRange("Y", 5,50, curr=24)
    app.addLabelScale("M")
    app.setScaleRange("M", 2,40, curr=5)
    app.addButton("Process GIF", doGif)
start()
# start the GUI
app.go()
