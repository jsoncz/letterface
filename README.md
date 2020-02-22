# letterface
![The GUI](https://i.imgur.com/bLAx1K6.png)
![Example](https://i.imgur.com/WO6DOho.mp4)
 originally an attempt to draw over a face with letters, like on a british passport photo.
I have only created this and experimented using Linux.

# Instructions
1 - make sure you have PIL and appjar installed (sudo pip install appjar)

2 use python3 app.py to start - check the required params (arguments) to use when loading
OR use the GUI by running: python3 gui.py 

Example: 
  #~/python3 app.py --i ./jason.png --x 11 --y 11 --size 10 --text 'LOVE'

3 - pictures are stored in the output folder

# Params
--i  [full path for the image to load]

--x  [x modulus, for manipulating the space between letters]

--y  [y ...same as above]

--size [size of the font]

--printargs [print the params on the top of the image for reference]

# TODO
improve the algos;
improve the printargs option;
have fun enjoying some python;
