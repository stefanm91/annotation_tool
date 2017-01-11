import Tkinter as tk  	# GUI 
import os	      	# system calls
from PIL import ImageTk, Image # images in GUI and image processing 
import dlib	      	# correlational tracker
from skimage import io 	# image read and conversion to array 
import glob		# some linux command functions
import numpy as np	# matlab python stuff
import cPickle		# saving rectangle pairs (list i/o)
import datetime		# date time function 
from sklearn.feature_extraction import image # just another image processing lib
import extract_patches	# for patch extraction?

class SampleApp(tk.Tk):  # inherit from Tk class 
    '''Illustrate how to drag items on a Tkinter canvas'''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        from ConfigParser import SafeConfigParser   # additonal parser lib

        config = SafeConfigParser()
        # [changeable]
        # location where config.ini is stored
        config.read(os.path.abspath("/media/deeplearning/BCB24522B244E30E/experiment_DL2/config.ini")) 

    
        # main folder where the experiment files are stored
        # change to main dir and afterwards use relative paths
        main_folder = config.get("Shared", "main_folder")
        os.chdir(main_folder)


	# set title you can do it in main as well
	self.title("Data annotation")
	
        # create a canvas
        self.canvas = tk.Canvas(width=1354, height=640) # size 
        self.canvas.pack(fill="both", expand=True)	# 
	
	
        # folder settings
        
        
        # path of where already extracted frames are stored
        self.video_folder = config.get("Training", "frames_location")
        
        # path of patches to be extracted
        # for non-patch approach, the content won't matter
        self.save_folder_patches = os.path.abspath("/media/deeplearning/BCB24522B244E30E/annotated_videos/23.12.2015_no_paper/frames/")
        
        # indicate where annotation.model is to be stored, e.g. annotations/annotation_training.model  (including filename)
        self.annot_save_folder = config.get("Training", "annotation_file_location")
        
        # for non-patch approach, the content won't matter
        self.save_folder_txt = os.path.abspath("/media/deeplearning/BCB24522B244E30E/annotated_videos/23.12.2015_no_paper/")
	
        # set image counter
        self.img_num = 0
        self.read_image_from_file()  # read figure in self.curr_photoimage
        self.create_photo_from_raw()
        
	self.total_num_of_frames = self.read_num_of_images()
	self.rectangle_frame_pairs = [0]*self.total_num_of_frames
	self.img_id = self.canvas.create_image(100, 100, image = self.curr_photoimage, anchor="nw") #, anchor = NW
	
	# this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}
	
        # create a couple movable objects
        self.polygon_id = 0
        
        # [changeable]
        # rectangle size in x and y
        self.rectangle_size = [100, 50]
        
        self.create_token((100, 100), "blue", self.rectangle_size) # in here tags="token" assigned 

	
        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.canvas.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)
        
        # add bindings for arrow keys when changing the image to right
        self.canvas.bind("<Return>", self.returnKey)
        self.canvas.bind("<Right>", self.rightKey)
        self.canvas.bind("<Left>", self.leftKey)
        self.canvas.bind("<Key-BackSpace>", self.backspaceKey)
        self.canvas.focus_set()
        
	# initialize tracker
	self.tracker = dlib.correlation_tracker()
	self.prev_tracker = self.tracker
	self.flag = 0
	
	'''create buttons section'''
	
	# add quit button
        button1 = tk.Button(self.canvas, text = "Quit", command = self.quit,
                                                            anchor = "w")
        button1.configure(width = 10)
        button1.pack()
        button1_window = self.canvas.create_window(10, 10, anchor="nw", window=button1)
	
	button2 = tk.Button(self.canvas, text = "Save annotations", command = self.save, anchor = "w")
	button2.configure(width = 15)
	button2.pack()
	button2_window = self.canvas.create_window(150, 10, anchor="nw", window=button2)
	
	# check if inbetween save and load the space is same
	button3 = tk.Button(self.canvas, text = "Load annotations", command = self.load, anchor = "w")
	button3.configure(width = 15)
	button3.pack()
	button3_window = self.canvas.create_window(330, 10, anchor="nw", window=button3)
	
	button4 = tk.Button(self.canvas, text = "Extract patches", command = self.extract_patches, anchor = "w")
	button4.configure(width = 15)
	button4.pack()
	button4_window = self.canvas.create_window(530, 10, anchor="nw", window=button4)
	
	#button5 = tk.Button(self.canvas, text = "Extract all patches", command = extract_patches.generate_patches_for_models((200,200)), anchor = "w")
	#button5.configure(width = 15)
	#button5.pack()
	#button5_window = self.canvas.create_window(530, 50, anchor="nw", window=button5)
	
	
	self.frame_info_label = tk.LabelFrame(self.canvas, text="Frame information", padx=5, pady=5)
	self.frame_info_label.pack()
	frame_info_label_window = self.canvas.create_window(800, 140, anchor="nw", window=self.frame_info_label)
	
	label_num_frames = tk.Label(self.frame_info_label, text="Frame #: 001/{0}".format(self.total_num_of_frames)) #, fg="red", font=('Helvetica',14), highlightbackground = "black", highlightthickness=1
	label_num_frames.pack()
	label_frame_path = tk.Label(self.frame_info_label, text="Frame folder: {0}".format(os.path.join(self.video_folder, "{0}.png".format(self.img_num+1))))
	label_frame_path.pack()
	
	self.frame_annot_label = tk.LabelFrame(self.canvas, text="Annotation information", padx=5, pady=5)
	self.frame_annot_label.pack()
	annot_info_label_window = self.canvas.create_window(800, 240, anchor="nw", window=self.frame_annot_label)
	
	label_annotated_frames = tk.Label(self.frame_annot_label, text="Annotated frames: 000/{0}".format(self.total_num_of_frames))
	label_annotated_frames.pack()
	
	label_annotation_folder = tk.Label(self.frame_annot_label, text = "Annotation folder: {0}".format(self.save_folder_txt))
	label_annotation_folder.pack()
	#print self.frame_info_label.winfo_children()[0].config(text="asdas")
        #label_num_frames_window = self.canvas.create_window(800, 140, anchor="nw", window=self.label_num_frames)
        """
        self.label_frame_path = tk.Label(self.canvas, text="Frame path:{0}".format(os.path.join(self.video_folder, "{0}.png".format(self.img_num+1))), fg="red", font=('Helvetica',14), highlightbackground = "black", highlightthickness=1)
	self.label_frame_path.pack()
        label_frame_path_window = self.canvas.create_window(800, 240, anchor="nw", window=self.label_frame_path)
	"""
	
	self.legend_label = tk.LabelFrame(self.canvas, text="Legend", padx=5, pady=5)
	self.legend_label.pack()
	legend_label_window = self.canvas.create_window(800, 340, anchor="nw", window=self.legend_label)
	
	legend_info = tk.Label(self.legend_label, text = "<--  Left \n --> Right \n ReturnKey <--| Annotate \n BackSpace < Delete Annotation ")
	legend_info.pack()	
	
	
	# insert label for frame ids
		
    def create_token(self, coord, color, rectangle_size):
        # Create a token at the given coordinate in the given color'''
        (x,y) = coord
	self.polygon_id = self.canvas.create_polygon(x-0,y-0,x+rectangle_size[0],y-0,x+rectangle_size[0],y+rectangle_size[1],x-0,y+rectangle_size[1], outline=color, fill='', tags="token")
    
    # or maybe use yield for reading next image
    def read_num_of_images(self):
        path_list = glob.glob(os.path.join(self.video_folder, "*.png"))

	return len(path_list)
	#img_raw = io.imread(f)
	#print len(img_raw)
	#print f
	#self.images_raw.append(img_raw)
	#self.images.append(ImageTk.PhotoImage(image = Image.fromarray(img_raw)))
	  
    def read_image_from_file(self, image_num = -1):
      # if no parameter is passed set to self.img_num + 1
      if (image_num == -1):
	image_num = self.img_num
      f = os.path.join(self.video_folder, "{0}.png".format(image_num+1))
      self.curr_image_raw = io.imread(f)
    
    def create_photo_from_raw(self):
      self.curr_photoimage = ImageTk.PhotoImage(image = Image.fromarray(self.curr_image_raw))
    
    def get_coord_rectangle(self):
      ''' Get coordinates of rectangle relative to image '''
      coords_rectangle = self.canvas.coords(self.polygon_id)
      coords_rectangle = [long(c) for c in coords_rectangle]
      coords_image = self.canvas.coords(self.img_id)
      coords_image = [long(c) for c in coords_image]
      coords_relative = [coords_rectangle[0]-coords_image[0],coords_rectangle[1]-coords_image[1],coords_rectangle[4]-coords_image[0],coords_rectangle[5]-coords_image[1]]
      
      return coords_relative      
    
    def change_image(self):
      # put here change rectangle  
      self.read_image_from_file()
      self.create_photo_from_raw()
      self.canvas.itemconfig(self.img_id, image = self.curr_photoimage)
      self.frame_info_label.winfo_children()[0].config(text = "Frame #: {0:0{width}}/{1}".format(self.img_num, self.total_num_of_frames, width = 3))
      self.frame_info_label.winfo_children()[1].config(text="Frame path: {0}".format(os.path.join(self.video_folder, "{0}.png".format(self.img_num+1))))
      if (self.rectangle_frame_pairs[self.img_num] == 0):
	self.canvas.itemconfig(self.polygon_id, outline = "blue")
      else:
	self.canvas.itemconfig(self.polygon_id, outline = "red") 
      
      counter = 0
      for x in self.rectangle_frame_pairs:
	if x is not 0:
	  counter = counter + 1
      
      self.frame_annot_label.winfo_children()[0].config(text="Annotated frames: {0:0{width}}/{1}".format(counter, len(self.rectangle_frame_pairs), width=3))
      
    def change_rectangle(self):
      rel_position = self.rectangle_frame_pairs[self.img_num]
      curr_position = self.get_coord_rectangle()
      #print (rel_position.left())
      self.canvas.move(self.polygon_id, -curr_position[0]+rel_position[0], -curr_position[1]+rel_position[1])
    
    
    #def split_train_test(self):
      
    
    # move the train = 0 out of this function
    def sliding_window(self, window_size, image_num = 0, overlap = 0, pos = 0):
           
      file_pos = os.path.join(self.save_folder_txt, "pos.txt")
      file_neg = os.path.join(self.save_folder_txt, "neg.txt")
      
      fop = open(file_pos, "a")
      fon = open(file_neg, "a")
      self.read_image_from_file(image_num)
      img = self.curr_image_raw

      coord_relative = self.rectangle_frame_pairs[image_num]
      coord_x = coord_relative[1]
      coord_y = coord_relative[0]
      p = 0
      counter = 0
      
      while p < (640/window_size[1])*(480/window_size[0]):
	Image.fromarray(img[coord_x:coord_x+50,coord_y:coord_y+100,:]).save("{0}/{1}_{2}.png".format(self.save_folder_patches,image_num,counter))
	if p == 0:
	  fop.write("patches/{0}_{1}.png 1 \n".format(image_num, counter))
	else:
	  fon.write("patches/{0}_{1}.png 0 \n".format(image_num, counter))
	  
	coord_y = coord_y+window_size[1]
	#proverka dali odi vo nov red, proveri na mal primer
	if coord_y >= 640-window_size[1]:
	  coord_x = coord_x+window_size[0]
	  coord_y = 0
	if coord_x >= 480-window_size[0]:
	  break
	
	p = p+1
	counter = counter + 1
      p = 0
      coord_x = coord_relative[1]
      coord_y = coord_relative[0]
      while p < (640/window_size[1])*(480/window_size[0]):
	coord_y = coord_y-window_size[1]
	# it should print it down for (0,0), 
	if coord_y < 0:
	  coord_x = coord_x-window_size[0]
	  coord_y = 640-window_size[1]
	if coord_x < 0:
	  break      
	
	Image.fromarray(img[coord_x:coord_x+50,coord_y:coord_y+100,:]).save("{0}/{1}_{2}.png".format(self.save_folder_patches,image_num,counter))
	fon.write("patches/{0}_{1}.png 0 \n".format(image_num, counter))

	p = p+1
	counter = counter + 1
      
      fop.close()
      fon.close()
      # or maybe instead of this, create non-overlapping windows, but that way it can miss
      # the positive sample
	
      # stavi tuka prefiksi na slikite
    
    
    #print self.patches.shape
    #for p in range(0,len(patches)):
      #im = Image.fromarray(patches[p])
      #im.save("test{0}.png".format(p))
      print "patches successfully saved for image: ", image_num 
    def extract_patches(self):
      # check for 0 in rectangles
      # count all zeros so you know how to split train and test
      # shuffle data
      # or maybe put NaN and count nans
      
      counter = 0
      for rect in self.rectangle_frame_pairs:
	if rect is not 0:
	  counter = counter + 1


      # split into training and test and save in file
      #stop_training = int(counter*0.75)
      stop_training = counter
      # this can go in one while document
      c = 0
      c1 = 0
      while c < stop_training:
	if self.rectangle_frame_pairs[c1] <> 0:
	  self.sliding_window ((50,100), c1, 0, 0)
	  c = c + 1
	c1 = c1+1
      
      while c < counter:
	if self.rectangle_frame_pairs[c1] <> 0:
	  self.sliding_window ((50,100), c1, 0, 1)
	  c = c+1
	c1 = c1+1
      
      # check verbose
      print "patches were saved congrats to you!!!"
      
      
      
      #self._sliding_window((50,100),0,0)
    
    
    
    def save(self):
      # on each update replace the same file
      # on each session create new file so there won't be overwrites
      
      
      f = file(os.path.join(self.annot_save_folder), 'wb')
      cPickle.dump(self.rectangle_frame_pairs, f, protocol = cPickle.HIGHEST_PROTOCOL)
      f.close()
      
      print "save was called!"
    
    # make Browse button
    def load(self):
      f = file(os.path.join(self.annot_save_folder), 'rb')
      previous_frames = cPickle.load(f)
      
      # in case extra frames are added
      #if len(previous_frames) == self.total_num_of_frames:
      self.rectangle_frame_pairs[0:len(previous_frames)] = previous_frames  
      
      f.close()
      
      #write message like successfully loaded etc.
      print "load was called"
    
    def rightKey(self, event):
      self.img_num +=1
      if self.img_num >= self.total_num_of_frames:
	self.img_num = 0
      
	# if rectangle exists redraw it
      if (self.rectangle_frame_pairs[self.img_num] is not 0):
	self.change_rectangle() 
      self.change_image()
      #print self.img_num/float(20*3600)
      
    
    # same code in both right and left key, refactor
    
    def leftKey(self, event):
      self.img_num -=1 
      if self.img_num < 0: 
	self.img_num = self.total_num_of_frames - 1
	# if rectangle exists redraw it
      if (self.rectangle_frame_pairs[self.img_num] is not 0):
	self.change_rectangle() 
      self.change_image()
    
    def returnKey(self, event):
        #self._sliding_window((50,100),0)
        #print self.img_num/float(20*3600)
        #save rectangle position
        self.rectangle_frame_pairs[self.img_num] = self.get_coord_rectangle()          
        #print image_id
        #print self._get_coord_rectangle()
        #print self.rectangle_frame_pairs
        
        
        # set the current position of the rectangle for tracking
	if (self.flag == 0):
	  
	  #print coords_rectangle
	  coords_relative = self.get_coord_rectangle()
	  
	  #proveri uste ednas koordinatite
	  self.tracker.start_track(self.curr_image_raw, dlib.rectangle(coords_relative[0],coords_relative[1],coords_relative[2],coords_relative[3]))
	  #self.tracker.start_track(self.images_raw[0], dlib.rectangle(170, 200, 240, 240))
	  self.flag = 1 
	  
	  self.img_num = self.img_num + 1
	  if self.img_num >= self.total_num_of_frames:
	    self.img_num = 0
	    
	  self.change_image()
	  
        else:
	  
        #self.new_img = ImageTk.PhotoImage(Image.open(os.path.join(self.video_folder, "{0}.png".format(self.img_num))))
	#self.img = io.imread(os.path.join(self.video_folder, "{0}.png".format(self.img_num)))
	#self.im_from_array = Image.fromarray(self.img)
	#self.new_img = ImageTk.PhotoImage(image = self.im_from_array)
	#self.canvas.itemconfig(self.img_id, image = self.new_img)

	  # you can refactor this code
	  coords_relative = self.get_coord_rectangle()
	  
	  #update filter
	  #self.prev_tracker = tracker
	  self.tracker.update(self.curr_image_raw, dlib.rectangle(coords_relative[0],coords_relative[1],coords_relative[2],coords_relative[3]))
	  
	  # update rectangle (overlay it)
	  rel_position = self.tracker.get_position()
	  curr_position = self.get_coord_rectangle()
	  #print (rel_position.left())
	  
	  # refactor this code as well
	  self.canvas.move(self.polygon_id, -curr_position[0]+rel_position.left(), -curr_position[1]+rel_position.top())
	  
	  self.img_num = self.img_num + 1
	  if self.img_num >= self.total_num_of_frames:
	    self.img_num = 0
	    
	  self.change_image()
	#print self.rectangle_frame_pairs
    def backspaceKey(self, event):
      self.rectangle_frame_pairs[self.img_num] = 0
      self.canvas.itemconfig(self.polygon_id, outline = "blue")

    
    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        
        # put item to front
        self.canvas.tag_raise(self._drag_data["item"])

    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def OnTokenMotion(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
