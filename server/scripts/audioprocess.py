# audioprocess.py
#
# This script provides an interface for dealing with audio processing
# using the pyAudioAnalysis library. It will be responsible for generating
# an arousal score, based on audio input.
#
# The load_model and load_data functions are "illusory" because
# the library is set up to call their function, so there isn't actually
# a model to return. To make it more typical on how we think about
# models though, we'll treat audioprocesser as a model object.

from pyAudioAnalysis import audioTrainTest as ATT
import numpy as np
import pandas as pd
import os

class audioprocessor:
  # class constructor
  def __init__(self, model_path=None, model_type=None, data_path=None):
    '''
      This is the constructor. If you don't pass any parameters, then
      it'll set it to a None state and you can set them later using the
      load functions. Once all parameters are loaded, you can call predict
      and be on your way.
    '''
    self.model_path = None
    self.model_type = None
    self.data_path = None
    self.dataset = None
    self.predictions = []
    if(model_path and model_type):
      self.load_model(model_path, model_type)

    if(data_path):
      self.load_data(data_path)

  # load the model
  def load_model(self, model_path, model_type):
    '''
      model_path: A path including the model name. Make sure to drop the 
                  suffix that follows an underscore, or else error! The
                  code will try to be flexible, but it's no guarantee.
                  Look, just don't name your model with underscores!
      model_type: Either 'svm' or 'randomforest'.
    '''
    self.model_path = model_path.split('_')[0]
    self.model_type = model_type

  # load the data
  def load_data(self, data_path):
    '''
      data_path: A path ending in '/' which is a folder containing all .wav
                 files. The code will try to be flexible if you forget, but
                 make sure you don't!
    '''
    if(data_path[-1]!='/'):
      data_path += '/'
    self.data_path = data_path
    folderitems = os.listdir(self.data_path)
    self.dataset = [fi for fi in folderitems if fi.endswith(".wav")]
    print(f"Dataset is {self.dataset}")

  # make predictions
  def predict(self):
    '''
      This function will predict ALL .wav files inside the specified folder.
      Please make sure to follow the specification in naming convention,
      as the library can be quite picky.
    '''
    # if all of these parameters are initialized
    print(f"data_path = {self.data_path}")
    if(self.model_path and self.model_type and self.data_path and self.dataset):
      predicted = []
      for data in self.dataset:
        print(f"Running {data} for {self.data_path+data}...")
        print(f"Model path is at {self.model_path}")
        print(f"Model type is {self.model_type}")
        prediction = ATT.file_regression(self.data_path+data, self.model_path, self.model_type)
        print(f"prediction completed.")
        predicted.append(prediction[0][0])

      self.predictions = [z for z in zip(self.dataset, predicted)]

    return self.predictions
