import scipy.io, os
import numpy as np
import cPickle
from PIL import Image
import shutil


def create_masks_for_model(annotated_model, mask_path, img_width, img_height):
  
 images_counter = 1
 file_name = annotated_model 
 annot = load_annotations_from_file(file_name)
 
 for x in range(0, len(annot)):
   arr = np.zeros((img_height, img_width))
   if (annot[x] <> 0):  
     arr[annot[x][1]:annot[x][3], annot[x][0]:annot[x][2]] = 1
     
     
     
   MM = {
      'PartMask' : arr
   }
           
   scipy.io.savemat(os.path.join(mask_path,"{0}.mat".format(images_counter)), mdict = {'MM': MM}, do_compression = True)
   images_counter = images_counter + 1 
   if (x % 1000 == 0 and x>=1000):
     print images_counter

def load_annotations_from_file(file_name):
  f = file(file_name, 'rb')
  frame_rectangle_pairs = cPickle.load(f)
  f.close()
  return frame_rectangle_pairs


