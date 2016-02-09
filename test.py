from sklearn.feature_extraction import image
import os
from skimage import io
from skimage.util.shape import view_as_windows
import numpy as np
from PIL import ImageTk, Image

#video_folder = os.path.abspath("/home/stefan/Documents/plexondata/2015_12_02_rat10/output/")
#img_raw = io.imread(os.path.join(video_folder,"1.jpg"))

#patches = view_as_windows(np.array(img_raw[:,:,0],(50,50))

#print patches.shape
coord_relative = [0,0]
window_size = [2,2]

one_image = np.arange(150).reshape((5,10,3))
patches = image.extract_patches_2d(one_image, window_size)

patch_nr = coord_relative[1]*(10-(window_size[1]-1))+coord_relative[0]
coord_x = coord_relative[1]
coord_y = coord_relative[0]
p = 0

print one_image
while p < (10/window_size[1])*(10/window_size[0]):
  coord_y = coord_y+window_size[1]
  #proverka dali odi vo nov red, proveri na mal primer
  if coord_y >= 10-window_size[1]:
    coord_x = coord_x+window_size[0]
    coord_y = 0
  if coord_x >= 10-window_size[0]:
    break
  #print coord_x, coord_y
  
  p = p+1
  
coord_x = 10
coord_y = 10
p = 0
while p < (10/window_size[1])*(10/window_size[0]):
  
  coord_y = coord_y-window_size[1]
  #proverka dali odi vo nov red, proveri na mal primer
  if coord_y < window_size[1] or coord_y < 0:
    coord_x = coord_x-window_size[0]
    coord_y = 10
    
  if coord_x < window_size[0] or coord_x < 0:
    break
  
  print coord_x, coord_y
  
  p = p+1

coord_x = 0
coord_y = 0
print one_image.shape
print coord_x+window_size[0]
print one_image[coord_x:coord_x+window_size[0],coord_y:coord_y+window_size[1],:]
#Image.fromarray(one_image[coord_x:coord_x+window_size[0],coord_y:coord_y+window_size[1],:]).convert("RGB").save("test.jpeg")



x = np.array([[1, 2, 3], [4, 5, 6]], np.int32)

im = Image.fromarray(x)
im.save('test.png')

