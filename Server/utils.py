import base64
import tensorflow as tf
import numpy as np
import cv2

XML_PATH = cv2.data.haarcascades
facesCascade = cv2.CascadeClassifier(XML_PATH + '/haarcascade_frontalface_default.xml')

IMG_SIZE = (96, 96)
FEMALE = 0
MALE = 1
judges = ['Average', 'Beautiful']

gender_model = None
beauty_model = None


def get_predicts(model, inputs):
  predictions = model.predict(inputs)
  predictions = tf.where(predictions >= 0.5, 1, 0).numpy().astype(np.int).flatten()
  return predictions


def detect_faces(image):
  coors = facesCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE)
  faces = []
  for (x, y, w, h) in coors:
    face = image[y:y+w, x:x+h]
    face = cv2.resize(face, IMG_SIZE)
    faces.append(face)

  return coors, np.array(faces)


def base64_str_to_cv2_img(base64_str):
  encoded_data = base64_str.split(',')[1]
  img_arr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
  img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  return img

def cv2_img_to_base64_str(img):
  _, buffer = cv2.imencode('.jpg', img)
  data = base64.b64encode(buffer)
  return data.decode('utf-8')


def predicts(data):
  img = base64_str_to_cv2_img(data)
  coors, faces = detect_faces(img)
  result = {
    "imgData": data,
    "errorCnt": 0,
    "non-face": True
  }
  
  if (len(faces) == 0):
    return result

  errorCnt = 0

  gender_predicts = get_predicts(gender_model, faces)
  beauty_predicts = get_predicts(beauty_model, faces)

  for idx, (x, y, w, h) in enumerate(coors):
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    if gender_predicts[idx] == MALE:
      text = "Sorry?"
      errorCnt += 1
    else:
      text = judges[beauty_predicts[idx]]

    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

  img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

  result['imgData'] = 'data:image/jpeg;base64,' + cv2_img_to_base64_str(img)
  result['errorCnt'] = errorCnt
  result['non-face'] = False

  return result


def load_resources():
  global gender_model, beauty_model
  global __class_to_name, __name_to_class

  print('Loading saved resources...')

  if gender_model is None:
    gender_model = tf.keras.models.load_model('../Experiments/gender_model.h5')
    beauty_model = tf.keras.models.load_model('../Experiments/beauty_model.h5')

  print('Saved resources loaded!')


# Demo
# if __name__ == '__main__':
  # load_resources()
  # test = ...
  # print(predicts([test]))