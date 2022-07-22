# eMosh (Emotional-Multimodality-Optical-Auditory-Synergy-Hub)


## Essence
We have essentially created a multimodal AI that can take visual and audio inputs from a live recorded input and can predict the emotion of the subject in the video, we use facial landmark detection, EMONET repo for processing the visual input, Audio Model that has been meticulously created with over 1200 annotations done by 4 taskers. We apply the late-fusion technique to merge the results of both to models and in the end try to infer the subject's emotions on the Russel's Circumplex of Emotionality and converting that information into easily understandable EMOJI (which pertains to the particular emotion shown)

## This is the repository containing:

1. Web Application allowing users to try wMosh predicting emoji and a corresponding valence and arousal on circumplex model
2. Web Server processing input movie to analyse the expexted valence, arousal and emoji through pre-trained audio model and EmoNet.

# Steps to run our app

## Special dependencies

1. You need a CUDA GPU on your machine in order to run our application.

2. You need to install torch. torch visions, torch audio by running
`pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113`


3. ffmpeg (a tool to convert webm to mp4)
Please install ffmpeg in your local machine.
For Windows: https://www.wikihow.com/Install-FFmpeg-on-Windows 
For Ubuntu: https://linuxize.com/post/how-to-install-ffmpeg-on-ubuntu-18-04/


## Web Application

1. Open up a terminal or command line.

2. Change your current working directory to my-app by
`cd my-app`

3. Install all necessary npm packages from running
`npm install`

4. Once all dependencies installed, run
`npm start`

5. The web application should start on your localhost:3000

## Web Server

1. Open up another terminal or command line window.

2. Change your current working directory to scripts by
`cd server/scripts`

3. Inside server dir, if you are Mac User, run
`bash ./initServer.sh`. If you are Windows users, run
`./initServer.bat`.

In order to run this command, you need to have pip installed on your machine. If you only have pip3, try replacing pip with pip3 inside .bat or .sh file.
Each shell script will install all required modules via pip and set some variables to run flask web server.

4. Web server should be up running now!

## FAQ -- Issues

After resetting our hardware to a clean stage as a new windows installation, we found some potential issues that might occur on a new python environment

1. Dlib cannot be installed because CMake is missing -> Solution is to install visual studio tools sdk and C++ CMake
2. FileNotFoundError [Err No 2] -> You need to install ffmpeg using the readme.md
3. If the duration cannot be found it is because the videos folder isn't cleared up as its iteration might have failed due to the issue above and it didn't clear the "videos" folder in "server"
4. Missing flask_cors -> Simply do pip install flask_cors or `python -m pip install flask_cors

# Self-Evaluation

Self evaluation

Outlined in our original goal, we wanted to create a model that can combine visual and audio
social signals to infer the emotional state of a human subject. To that end, our model was able to
combine these two components through a late fusion approach using the Circumplex model as a base.

We originally planned to create a real-time web application where users can interact with a responsive avatar or emoji based on the arousal and valence extracted from their facial expressions and voices. However, due to the limitation of hardware we could access and the speed of EmoNet predictions, it was infeasible to implement a real-time app. Therefore, we changed our app allowing users to record or upload a short movie, and the trained models will compute the predicted valence and arousal from it. In short, our application will detect the most striking emotion detected in a short movie clip and express it via an emoji and a coordinate of valence and arousal. It would be much more interesting if we could optimize EmoNet and make avatar changing as users's expression changes in the future. 

Our approach was experimental and not as thorough as we would have liked, and due to limitations of data
and annotation, our results could have been better. With that said, we were able to identify weaknesses
in the current state-of-the-art models and representations, and recommend areas of interest to explore.

Given more time, we would have liked to find larger samples of datasets including more extreme emotions
as well as naturalistic data so that we may get a more balanced representation of emotional expression.
Furthermore, another improvement we can make is to take a more rigorous formulation of our experimental
procedure by using more advanced statistical methods of quantifying results.

Changes to the original plan was the introduction of pyAudioAnalysis, which we used SVM and random forests
instead of a CNN due to the implementation of the library. We were able to compare models and find how
each performs under different annotation aggregation methods. We were able to get a respectable error of around
20% of the range using random forests, which was one of our goals. We also believe that the generated emojis
are qualitatively similar to what the input would expect.

# Extra Credits 
https://github.com/face-analysis/emonet (The actual CNN model for visual input)

# Co-Authors: 

Tanishk Sharma <br>
John Chan <br>
Kodai Hiraishi <br>
Sam Su Zhou <br>


