#!/usr/bin/python
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
# This example shows how to use the correlation_tracker from the dlib Python
# library.  This object lets you track the position of an object as it moves
# from frame to frame in a video sequence.  To use it, you give the
# correlation_tracker the bounding box of the object you want to track in the
# current video frame.  Then it will identify the location of the object in
# subsequent frames.
#
# In this particular example, we are going to run on the
# video sequence that comes with dlib, which can be found in the
# examples/video_frames folder.  This video shows a juice box sitting on a table
# and someone is waving the camera around.  The task is to track the position of
# the juice box as the camera moves around.
#
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#   or
#       python setup.py install --yes USE_AVX_INSTRUCTIONS
#   if you have a CPU that supports AVX instructions, since this makes some
#   things run faster.  
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake and boost-python installed.  On Ubuntu, this can be done easily by
#   running the command:
#       sudo apt-get install libboost-python-dev cmake
#
#   Also note that this example requires scikit-image which can be installed
#   via the command:
#       pip install scikit-image
#   Or downloaded from http://scikit-image.org/download.html. 

import os
import glob

import dlib
from skimage import io

import Tkinter as tk
 
def showxy(event):
    xm, ym = event.x, event.y
    str1 = "mouse at x=%d  y=%d" % (xm, ym)
    # show cordinates in title
    root.title(str1)
    # switch color to red if mouse enters a set location range
    x,y, delta = 100, 100, 10
    frame.config(bg='red'
                 if abs(xm - x) < delta and abs(ym - y) < delta
                 else 'yellow')
 
root = tk.Tk()
frame = tk.Frame(root, bg= 'yellow', width=300, height=200)
frame.bind("<Motion>", showxy)
frame.pack()
 
root.mainloop()

# Path to the video frames
#video_folder = os.path.join("..", "03_01_2016-2", "0")
video_folder = os.path.abspath("/home/stefan/Documents/plexondata/2015_12_02_rat10/output/0/0/")
# Create the correlation tracker - the object needs to be initialized
# before it can be used
tracker = dlib.correlation_tracker()

win = dlib.image_window()
# We will track the frames as we load them off of disk
for k, f in enumerate(sorted(glob.glob(os.path.join(video_folder, "*.jpg")))):
    print("Processing Frame {}".format(k))
    img = io.imread(f)

    # We need to initialize the tracker on the first frame
    if k == 0:
        # Start a track on the juice box. If you look at the first frame you
        # will see that the juice box is contained within the bounding
        # box (74, 67, 112, 153).
        #tracker.start_track(img, dlib.rectangle(50, 20, 100, 30))
        #tracker.start_track(img, dlib.rectangle(330, 330, 400, 370))
        tracker.start_track(img, dlib.rectangle(170, 200, 240, 240))
    else:
        # Else we just attempt to track from the previous frame
        tracker.update(img)
    #if k == 5:
        #tracker.update(img, dlib.rectangle(330, 330, 400, 370))
    #if k == 38:
	#tracker.update(img,dlib.rectangle(168+80, 208, 236+80, 246))
    print tracker.get_position()
    win.clear_overlay()
    win.set_image(img)
    win.add_overlay(tracker.get_position())

    dlib.hit_enter_to_continue()
    
