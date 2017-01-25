# Annotation Tool used for Deep Tracking

Semi-manual video annotation tool based on correlation tracker.
The correlation tracker works by combining filters for translation and scaling so it can detect the object at different sizes and
different locations. It manages to mark the object in the clear situations but does not perform accurately in all cases.

Please visit the project [web page](http://www.optophysiology.uni-freiburg.de/Research/Deep-Tracking) for more details.

[1] Shahbaz Khan Danelljan Haeger. Accurate scale estimation for robust visual tracking. In: BMVC (2014).

# HowTo use the tool
Annotation of the data can be done by positioning a rectangle around the object to indicate the objects's location. 
The annotation data is necessary to later train deep neural networks. (This way the network can be 'told' where the object is (supervised learning) in each training image).

# Video preperation
Before annotation is done, the video segments where the object of interest is visible has to be selected manually and than the frames where movement of the object is present has to be extracted from the video. Once the extraction is done, it can be proceeded with annotation.

1.	Copy training and test videos to folder /experiment_DL/videos

2.	Create files segments_{video}.txt for each video that you want to be used for training or testing in the following directory /experiment_DL/segments

	{video} can e.g. be training or validation, does not have to be video name. In this tutorial, there are two videos, one for training and one for testing, so two files are present: segments_Training.txt and segments_Test.txt

3.	Play videos and mark segments in the previously created files where the object is visible in the following format {hh}:{mm}:{ss}. For example, if the object is visible and moving at minute 20 and 34 sec from the video, the format will look like 00:20:34. All of the segments has to be inserted one after another in new lines, as follows:
00:20:34
00:21:45
00:22:34
Note: For each video there should be separate segments_{video}.txt file. In the training case segments_Training.txt was used. For testing use segments_Test.txt

4.	Now, next step is to extract the frames from the segmented videos. The frames are split into training and testing frames. For this reason, two scripts called extract_frames_from_segments_training.py and  extract_frames_from_segments_test.py exist. Navigate to /annotation_tool to find the above mentioned scrips.

5.	First, open extract_frames_from_segments_training.py and change the appropriate variables where the tag [changeable] is present.  If you have one training video, leave images_counter as it is, otherwise change it to the number of last frame present in the training folder (if you had previously extracted frames from another video the frame numbers should continue from where they stopped). Start the script with python extract_frames_from_segments_training.py
After the extraction the extracted frames are stored in:
<DIR>/experiment_DL/frames/training

6.	Now, repeat step 1-5 for a testing video but use the script extract_frames_from_segments_test.py instead for extracting the frames.
After the extraction the extracted frames are stored in:
<DIR>/experiment_DL/frames/test

7.	Repeat steps 1-6 for all the training/testing videos.

# HowTo extract patches
To start the annotation tool, run main_training.py by opening Terminal, navigating to <DIR>/annotation_tool and writing the command python main_training.py. Annotate the data and press on the button Save Annotations. 

# HowTo generate image masks
1.	First annotation of the previously extracted training frames will be done.
To start the annotation tool, run main_training.py by opening Terminal, navigating to <DIR>/annotation_tool and writing the command python main_training.py. Annotate the data and press on the button Save Annotations
2.	After annotation of the frames is done, next step is to compute the segmentation masks from the annotations. For that reason, navigate to <DIR>/annotation_tool/ and open compute_masks_training.py using editor. There is variable images_counter that should be changed to the last mask number present in the folder. The reason for this is same as before, to preserve numbering of the masks when multiple videos are annotated.
3.	Next, run compute_masks_training.py by using the command python compute_masks_training.py to compute the masks in the selected masks folder.
4.	Now, repeat step 1-5 for a testing video by use the script main_test.py and compute_masks_test.py
5.	Repeat the whole process using all testing/training videos
