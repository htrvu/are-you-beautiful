from flask import Flask, request, jsonify
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app)

@app.route('/judge_imgs', methods=['GET', 'POST'])
def classify_image():
  data = request.get_json()
  result = utils.predicts(data["imgData"])
  response = jsonify(result)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

if __name__ == '__main__':
  print('Starting Python Flask Server...')
  utils.load_resources()
  app.run(port=5000)

