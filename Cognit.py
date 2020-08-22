from flask import Flask, redirect, url_for, request, render_template, flash
from urllib.request import urlopen
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import requests

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
   if request.method == 'POST':
      name = request.form['nm']
      return redirect(url_for('success',name = name))
   return render_template('index.html' )

@app.route('/success')
def success():
   image = request.args.get('name', None)
   ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"
   prediction_key = "4c99a663c6984df6b912025e2c7e1dee"
   my_project_id = "c9f9158e-e82d-4541-926a-15699c59a4b4"
   publish_iteration_name = "Iteration3"

   test_data = urlopen(image).read()
   prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
   predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
   results = predictor.detect_image(project_id=my_project_id, published_name=publish_iteration_name, image_data=test_data)
   first_value = 0
   maximum = 0
   print (first_value)

   for prediction in results.predictions:
      next_value = int(prediction.probability*100)
      if maximum <= next_value:
        maximum = next_value
        tag = prediction.tag_name
      print(int(prediction.probability*100))
      print(maximum)
      print(tag)
      print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height))
   return tag

if __name__ == '__main__':
   app.run(debug = True)