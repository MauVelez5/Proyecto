import streamlit as st
import paho.mqtt.client as paho
import time
import json
import cv2
import numpy as np
#from PIL import Image
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker,port)

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("Inicio de sesión")

img_file_buffer = st.camera_input("Toma una Foto")
st.markdown("""<style>.stApp {background-color: #4e93fa;  /* Cambia este valor al color de fondo que desees */}</style>""",unsafe_allow_html=True)
if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
   #To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0]>0.6:
      st.header('Hola Mauricio')
      client1.publish("IMIA","{'gesto': 'Abre'}",qos=0, retain=False)
      time.sleep(0.2)
    if prediction[0][1]>0.6:
      st.header('Hola Santiago')
      client1.publish("IMIA","{'gesto': 'Cierra'}",qos=0, retain=False)
      time.sleep(0.2) 
    if prediction[0][2]>0.6:
      st.header('No es reconocible, vuelva a intentar')
      client1.publish("IMIA","{'gesto': 'Cierra'}",qos=0, retain=False)
      time.sleep(0.2)  
