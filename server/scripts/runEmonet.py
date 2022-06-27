#This is the runnable for EmoNet,
#This file handles the input and sends it to the EmoNet object

from EmoScoreModule import EmoScore
from skimage import io
import os

def emonetDriver(path):
    path = path + "/"
    print("Here is a path = ", path)
    contents = os.listdir(path)
    vidpath = path + contents[0]
   
    #Instantiating an Emonet Object

    EmoObj = EmoScore();

    #valence, arousal = EmoObj.calculateVA(newImage); #forIMAGE (Not required)
    #plot(valence, arousal)

    valence, arousal = EmoObj.parseVideo(vidpath); #forVideo
    return (valence, arousal)