import os, sys, time, random
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

#couter for the Text string loop that comes later
count = 0
altcount = 0
#original size of image when Loaded
origheight=0
origwidth=0
#final GIF Path (global variable)
gifpath=''

#functions
def makeGif(image, frames, dur, xmod, ymod, reverse, magic, fontsize, fontgrow, mystring, altstring, shrink):
    global gifpath
    print("frames, dur, xmod, ymod, reverse, magic, fontsize, fontgrow, mystring, altstring, shrink")
    print(frames, dur, xmod, ymod, reverse, magic, fontsize, fontgrow, mystring, altstring, shrink)
    #convert to RGB for grabbing pixel data easier later
    rgb_im = image.convert('RGB')
    if shrink == True:
        maxsize = (origheight/2, origwidth/2)
        image.thumbnail(maxsize)

    images = []
    for i in range(frames):
        images.append(Image.new(mode = "RGB", size = (image.size[0], image.size[1])))
        images[i].convert('RGB')
        if fontgrow==True:
            if i > round(frames/2):
                fontsize+=magic

        if reverse==True:
            if i >= round(frames/2):
                if xmod<5:
                    xmod+=magic
                if ymod<5:
                    ymod+=magic
        else:
            ymod+=1
            xmod+=1

        #get pixel RGB information
        for j in range(image.size[0]):
            for k in range(image.size[1]):
                if k % xmod== 1:
                    if j % ymod== 1:
                        drawpixel(image, j,k, ImageDraw.Draw(images[i]),fontsize, mystring, altstring, magic)

                #WATERMARK
        #ImageDraw.Draw(images[i]).text((10,250),"LetterFace",(255,255-i*4,255-i),ImageFont.truetype("./Sansation_Bold.ttf", 80))
        #ImageDraw.Draw(images[i]).text((100,350),"  by Jason B",(250,255,255-i),ImageFont.truetype("./monof555.ttf", 40))

        if shrink==True:
            images[i].thumbnail(maxsize)
        images[i].save('./output/'+str(i)+'.jpg')
    #after the loop for each frame processed, lets try to make the gif
    gifpath='./GIFS/'+time.strftime("%Y%m%d-%H%M%S")+'.gif'

    images[0].save(gifpath, format='GIF',
               append_images=images[1:],
               save_all=True,
               duration=dur, loop=0)

##Main Drawing function
def drawpixel(image, i,j, imgdraw, fontsize, mystring, altstring, magic):
    #font = ImageFont.truetype("./chinese.ttf", fontsize)
    font = ImageFont.truetype("./monof555.ttf", fontsize)
    global count
    global altcount
    if count==len(mystring)-1:
        count=0
    else:
        count+=1
    if altcount==len(altstring)-1:
        altcount=0
    else:
        altcount+=1
    #Amazing algo to print the string in a loop, Buddha - maybe I am stupid but this is the way I found
    #convert to RGB for grabbing pixel data easier later
    rgb_im = image.convert('RGB')
    r, g, b = rgb_im.getpixel((i, j))
    if b <=magic*7:
        imgdraw.text((i, j),mystring[count],(r,g,b),font=font)
    else:
        imgdraw.text((i, j),altstring[altcount],(r,g,b),font=font)



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
    global image, origheight, origwidth
    file=app.openBox(title="Choose an Image", dirName=None, fileTypes=[('images', '*.png'), ('images', '*.jpg')], asFile=False, parent=None, multiple=False, mode='r')
    #load / open the image
    image = Image.open(file)
    origheight = round(image.size[0])
    origwidth = round(image.size[1])
    app.setLabel("loaded", file+" Image Loaded")
    app.setLabelBg("loaded", "blue")

def doGif(btn):
    global gifpath, count, altcount
    count = 0
    altcount = 0
    frames=app.getScale("Animation Frames")
    dur=app.getScale("Animation Duration")
    mystring=app.getEntry("Text String")
    altstring=app.getEntry("Alt String")
    x=app.getScale("X")
    y=app.getScale("Y")
    magic=app.getScale("M")
    reverse=app.getCheckBox("Alt Flow")
    fontsize=app.getScale("Font Size")
    fontgrow=app.getCheckBox("Grow Font")
    shrink=app.getCheckBox("Shrink GIF")
    if altstring == "":
        altstring = ".";
    if mystring != "":
        app.setLabelBg("loaded", "blue")
        makeGif(image, frames, dur, x, y,reverse, magic, fontsize, fontgrow, mystring, altstring, shrink)
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
    app.showScaleValue("Animation Frames", show=True)
    app.addLabelScale("Animation Duration")
    app.setScaleRange("Animation Duration", 20,250, curr=40)
    app.showScaleValue("Animation Duration", show=True)
    app.addLabelEntry("Text String")
    app.addLabelEntry("Alt String")
    app.addCheckBox("Grow Font")
    app.addCheckBox("Alt Flow")
    app.addCheckBox("Shrink GIF")
    app.addLabel("options", "Modifiers")
    app.setLabelBg("options", "orange")
    app.addLabelScale("Font Size")
    app.setScaleRange("Font Size", 5,60, curr=15)
    app.showScaleValue("Font Size", show=True)
    app.addLabelScale("X")
    app.setScaleRange("X", 5,40, curr=24)
    app.addLabelScale("Y")
    app.setScaleRange("Y", 5,40, curr=24)
    app.addLabelScale("M")
    app.setScaleRange("M", 2,20, curr=5)
    app.addButton("Process GIF", doGif)
start()
# start the GUI
app.go()
