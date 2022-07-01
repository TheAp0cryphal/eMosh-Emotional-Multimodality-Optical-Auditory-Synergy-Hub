# from crypt import methods
from flask import Flask, request
from flask_cors import CORS
import json

from driver import module_manager


import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route("/test", methods=['GET'])
def test():
   return "<p>test</p>"

@app.route("/upload_video", methods=['POST'])
def upload_video():
   uploaded_video = request.files['video']
   app.logger.info(uploaded_video.filename)
   app.logger.info(uploaded_video.mimetype)
   result = module_manager(uploaded_video)
   JsonObject = json.dumps(result)
   return JsonObject

@app.route("/upload_image", methods=['POST'])
def upload_image():
   uploaded_image = request.files['image']
   app.logger.info(uploaded_image.filename)
   return "<p>image received</p>"
