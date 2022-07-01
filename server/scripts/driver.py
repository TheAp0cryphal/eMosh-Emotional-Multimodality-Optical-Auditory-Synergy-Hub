# driver.py
#
# This is the main script file that will interact with:
# 1. The front end GUI
# 2. The processing modules
# 3. The fusion module
#
# The front end GUI will provide a video clip.
# This video clip will have audio extraction done by audioextract.py
# The audio is then processed by audioprocess.py
# The video clip will be individually processed by emonet.py
# From audioprocess and emonet, we will obtain a valence and arousal
# score. This score will be passed into fusion.py, which will return
# an emoji code. This code will then be passed back to the front end
# for display.
#
# We should define a conventional file-structure. All paths and folders
# will follow this convention. Refer to the following:
#
# ./root/
#       scripts/
#           driver.py
#           audioextract.py
#           audioprocess.py
#           fusion.py
#           emonet.py
#       videos/
#           video1.avi
#           video2.mp4
#       audio/
#           audio1.wav
#           audio2.wav
#       audiomodel/
#           AudioPredictModel_annotate_with_means
#           AudioPredictModel_annotate_with_meansMEANS

# We will start with the necessary imports

import subprocess
from audioprocess import audioprocessor
from audioextract import audioextract
from fusion import fusion
from runEmonet import emonetDriver
import os
from pathlib import Path
from emonet import *

dirname = os.path.dirname(__file__)
dirPath = Path(dirname)

def module_manager(video):
    # First, let's define all the paths we need
    
    video_path = "../videos"
    audio_path = "../audio"
    audiomodel_path = "../audiomodel/"

    file_name, file_extension = os.path.splitext(video.filename)

    file_location = dirPath.parent / video_path[3:len(video_path)] / video.filename

    print(file_location)

    video.save(file_location)

    if('webm' in file_extension):      
        mp4_filename = file_name + '.mp4'
        mp4_file_location = os.path.join(video_path, mp4_filename)
        print("file_location =", file_location, "mp4_file_location =", mp4_file_location)
        subprocess.run(['ffmpeg', '-i', file_location, mp4_file_location])
       
        if os.path.exists(file_location):
            os.remove(file_location)
    
    # First, we will do preprocessing by audio extraction
    print(f"DEBUG: We begin by extracting the audio from video")
    audioextract(video_path, audio_path)

    # We will next process the audio - begin with
    print(f"DEBUG: We will now process the audio")
    model_type = "randomforest"
    model_name = "AudioPredictModel"
    model_input = audiomodel_path + model_name
    processor = audioprocessor(model_input, model_type, audio_path)

    # Let's set a fusion ratio for arousal.
    ratio = 0.35

    # Call the predict function to start predicting
    print(f"DEBUG: Data has been loaded, now actually predict.")
    audioresults = processor.predict()

    # The return values are [(audioname, prediction), ...]
    # We are interested in a singular value to display, so:
    if(audioresults):
        # if an audio file gets generated, then extract results
        audio_result = audioresults[0][1]
        print(f"DEBUG: audioarousal = {audio_result}")
    else:
        audio_result = 0
        ratio = 0

    # Finally, we perform fusion.
    # We make an assumption: var audio_result contains the arousal, raw number
    # and var emonet_result is a tuple (valence, arousal)

    emonet_result = emonetDriver(video_path)
    #print (emonet_result[0], emonet_result[1])

    fuser = fusion(ratio)

    # We'll now get the coordinates from the fuser
    coords = fuser.fuse(emonet_result, audio_result)
    emoji = fuser.coord_to_emoji(coords)

    #plot (coords[0], coords[1])

    print(coords, emoji)
     # find the items inside the folder
    contents_video = os.listdir(video_path)
    contents_audio = os.listdir(audio_path)

    # We now want to return the emoji back to the front end...
    # ----- code needed -----
        # remove all items in video folder
    for content_video in contents_video:
        os.remove(video_path+"/"+content_video)

    # remove all items in the audio folder
    for content_audio in contents_audio:
        os.remove(audio_path+"/"+content_audio)
        
    return (coords, emoji)
# -----------------------

