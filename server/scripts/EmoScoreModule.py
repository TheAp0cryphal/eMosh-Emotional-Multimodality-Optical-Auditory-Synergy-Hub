#This scripts bridges the emonet object and necessary functions for augmentations, 
#landmark detection and calculating the
#valence and arousal from the input

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import dlib
import numpy as np
import torch
from torchvision import transforms 
from pathlib import Path
from emonet.emonet.models import EmoNet
from emonet.emonet.data_augmentation import DataAugmentor
from skimage import io
import math


#The EmoScore class holds the functions
class EmoScore:

  #init handles loading the pre-trained model and setting the device usage to CUDA as that is 
  #necessary to run predictions.

  def __init__(self):    
    
    self.n_expression = 8
    self.device = 'cuda:0'

    state_dict_path = os.getcwd() + "/emonet/pretrained/emonet_8.pth"
    state_dict = torch.load(str(state_dict_path), map_location='cpu')
    state_dict = {k.replace('module.',''):v for k,v in state_dict.items()}
    self.net = EmoNet(n_expression=self.n_expression).to(self.device)
    self.net.load_state_dict(state_dict, strict=False)
    self.net.eval()
    
  def landmarkCalculator(self, Image): 
                        
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(os.getcwd() + "/shape_predictor_68_face_landmarks.dat") 

    #This file is available in the scripts folder, it is essentially the model that detects facial landmarks.

    grayscale = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
    
    #Setting the detector on the grayscale image (grayscaling improves detection accuracy for our model)
    rects = detector(grayscale, 1)

    shape = None;

	
    #Getting the landmark coordinates from the predictor

    for rect in rects:
      shape = predictor(grayscale, rect)
    shape_np = np.zeros((68, 2), dtype = "int")

    #If a frame cannot find a face, it simply sends in a value that wouldnt effect the result
    if shape == None:
      return [0, 0, 0, 0]

    #Imposing the landmark data on the image    
    for i in range (0,68):
      shape_np[i] = (shape.part(i).x, shape.part(i).y) #If nonetype error, Error detecting face
    shape = shape_np;

    for i, (x, y) in enumerate(shape):
        cv2.circle(Image, (x, y), 2, (0, 0, 255), -1)

    print ("\n\n")

  
    landmarks = shape

    #Cropping the image bbox to the source face on the basis of landmarks maximums and minimums

    bounding_box = [landmarks.min(axis=0)[0], landmarks.min(axis=0)[1],
                landmarks.max(axis=0)[0], landmarks.max(axis=0)[1]]

    return bounding_box
    
  def calculateVA(self, Image): #for Single Image, if parsing video, look at function below. It calls calculateVA on each frame.

      image_size = 256

      # loading data part
      transform_image_shape_no_flip = DataAugmentor(image_size, image_size) 
      transform_image = transforms.Compose([transforms.ToTensor()])

      print("Shape of the input = ", Image.shape)
      assert(Image.ndim==3 and Image.shape[2]==3), "There is an issue with the file that was passed \n Troubleshoot: \n 1. Check if the face has clear boundaries in the image \n2. Check that the face is not obstructed."

      bbox = self.landmarkCalculator(Image)

      if bbox == [0, 0, 0, 0]:
        return 0, 0

	#Performing augmentations on the image to transform it, as the net requires
      image, _ = transform_image_shape_no_flip(Image, bb = bbox) 
      image = transform_image(image)
	
	#Manipulating the tensor to add a dimension for emonet to understand its batch

      inputImage = image[None, :] #Adding a tensor dimension to the image [:,:,:] -> [:,:,:,:]
      inputImage = inputImage.to(self.device)

      print(f'\nFrame Successful!')
      print(f'-----------------')

	#Predicting on the image/frame

      out = self.net(inputImage)

	#Extracting the data out from the tuple
      valence = out['valence'].item()
      arousal = out['arousal'].item()

      return valence, arousal

  
  def sorting(self, numbers_array):
	  #Sorting numbers in ascending, without regard of its actual sign
        return sorted(numbers_array, key=abs)

  def parseVideo(self, path):
      capture = cv2.VideoCapture(path) # Video Path
      fps = capture.get(cv2.CAP_PROP_FPS)  
      frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) #number of frames from the video

      valences = []
      arousals = []

      skipTheseManyFrames = math.floor(frame_count / 10) #Diving by 10 to enforce time consistency across different frame counts

      i = 0
      frameCounter = 0

      while (True):
        
        frameCounter = frameCounter + 1
        print ("Progress = ", frameCounter, "/", frame_count)
        
        i = i + 1
	  #Grabbing a frame to skip it.
        _ = capture.grab()

        #Once i reaches the threshold, it resets to 1
        if i >= skipTheseManyFrames:
          i = 1
          success, img = capture.read() 

          if success == True:
            valence, arousal = self.calculateVA(img)
            valences.append(valence)
            arousals.append(arousal)
          else:
		#Loop Breaker, breaks when no more frames can be read!
            break;

      sortedArousals = self.sorting(arousals)
      sortedValences = self.sorting(valences)

    
      pop_times = math.floor(len(sortedArousals)/3) # picking the top thirds of the outputs!

      vAvg = []
      aAvg = []
	
	#Popping the highest values of the list, depending on video frames, the ratio would be decided by the function 
	#for pop_times

      for i in range (pop_times):
        v = sortedValences.pop()
        a = sortedArousals.pop()

        vAvg.append(v)
        aAvg.append(a)
	
      assert (pop_times > 0), "The video does not have enough frames, please record a longer video"
	#Returning avg of the x top frame val, arousal values.
      return (sum(vAvg)/pop_times, sum(aAvg)/pop_times)