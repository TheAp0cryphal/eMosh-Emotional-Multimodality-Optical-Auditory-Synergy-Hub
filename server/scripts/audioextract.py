# audioextract.py
#
# Script for converting video into audio found inside a directory.
# moviepy - open-source moviepy library

import moviepy.editor as mp
import os

# script for extracting audio from video
def audioextract(video_file_path, audio_file_out_path):
  # we'll do a little bit of sanitation
  if(not video_file_path.endswith("/")):
    video_file_path += '/'

  if(not audio_file_out_path.endswith("/")):
    audio_file_out_path += '/'
  
  contents = os.listdir(video_file_path)
  for content in contents:
    if(content.endswith(".mp4") or content.endswith(".avi") or content.endswith(".webm")):
      clipname = content.split('.')[0]
      clip = mp.VideoFileClip(f"{video_file_path}{content}")
      if clip.audio != None:
        clip.audio.write_audiofile(audio_file_out_path+f"{clipname}.wav", verbose=False, logger=None)
        clip.close()
        
      # depends on which version pip installs, either use progress_bar=False or logger=None
      
