import os
import shutil
from ConfigParser import SafeConfigParser

config = SafeConfigParser()


# [changable] 
# complete path of video and the filename
video_path = "/media/deeplearning/BCB24522B244E30E/experiment_DL/videos/20160414001_1_Rat38_take1.AVI"

# [changable]
# path where frames should be extracted
frames_path = "/media/deeplearning/BCB24522B244E30E/experiment_DL/frames/training/"

# [changeable]
# set to last number + 1 of the frame that is in folder frames_path
# if the folder frames_path is empty leave it to 1
images_counter = 1

counter = 1

# [changable]
# path and filename  where segment information  are stored
with open("/media/deeplearning/BCB24522B244E30E/experiment_DL/", "r") as ins:
    array = []
    for line in ins:
       # read segments from file and skip the newlines
       no_newline = line[0:len(line)-1]
       new_path = frames_path + "model" + str(counter) + "/"
       
       # create temporary folder so all segments can be extracted there and than copied
       # with the consecutive name  ... , 10034, 10035, ... in the frames_path       
       os.system("mkdir " + new_path)
       
       # [changeable][optional] 
       # 00:00:02 indicates number of seconds to take from starting point        
       os.system("ffmpeg -i " + video_path + " -ss " + no_newline + " -t 00:00:02 -qscale:v 2 -r 80 -f image2 '" + new_path + "%d.png'")
       counter = 1
       for f in os.listdir(new_path):
         shutil.copy2(os.path.join(new_path, "{0}.png".format(counter)), os.path.join(new_path, "../", "{0}.png".format(images_counter)))   
         images_counter = images_counter + 1
         counter = counter + 1
       os.system("rm -R " + new_path)

       
    
