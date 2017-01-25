# Annotation Tool used for Deep Tracking

Semi-manual video annotation tool based on correlation tracker.
The correlation tracker works by combining filters for translation and scaling so it can detect the object at different sizes and
different locations. It manages to mark the object in the clear situations but does not perform accurately in all cases.

Please visit the project [web page](http://www.optophysiology.uni-freiburg.de/Research/Deep-Tracking) for more details.

[1] Shahbaz Khan Danelljan Haeger. Accurate scale estimation for robust visual tracking. In: BMVC (2014).

# HowTo use the tool
Annotation of the data can be done by positioning a rectangle around the object to indicate the objects's location. 
The annotation data is necessary to later train deep neural networks. (This way the network can be 'told' where the object is (supervised learning) in each training image).

# HowTo extract patches


# HowTo generate image masks
1.	First annotation of the previously extracted training frames will be done.
To start the annotation tool, run main_training.py by opening Terminal, navigating to <DIR>/annotation_tool and writing the command python main_training.py. Annotate the data and press on the button Save Annotations
2.	After annotation of the frames is done, next step is to compute the segmentation masks from the annotations. For that reason, navigate to <DIR>/annotation_tool/ and open compute_masks_training.py using editor. There is variable images_counter that should be changed to the last mask number present in the folder. The reason for this is same as before, to preserve numbering of the masks when multiple videos are annotated.
3.	Next, run compute_masks_training.py by using the command python compute_masks_training.py to compute the masks in the selected masks folder.
4.	Now, repeat step 1-5 for a testing video by use the script main_test.py and compute_masks_test.py
5.	Repeat the whole process using all testing/training videos
