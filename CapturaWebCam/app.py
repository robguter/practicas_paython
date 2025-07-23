from email import message
from urllib import response
import cv2
import time
import base64
from dotenv import load_dotenv

from flask import Flask, request, render_template

load_dotenv()

app = Flask(__name__)

def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

def capture_image(camera_index):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    time.sleep(0.5)
    if not cap.isOpened():
        print("No se puede abrir el dispositivo de video")
        return None
    ret, frame = cap.read()
    if ret:
        filename = "static/captured_image.jpg"
        cv2.imwrite(filename, frame)
        print(f"Imagen guardada como {filename}")
        return filename
    else:
        print(f"Error al capturar la Imagen")
        return None

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analizar_foto(image_path):
    from openai import OpenAI
    base64_image = encode_image(image_path)
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role" : "User",
                "content" : [
                    {"type" : "text", "text" : "Describe la imagen en detalle"},
                    {
                        "type" : "image_url",
                        "image_url" : {
                            "url" : f"data:image/jpeg;base64,{base64_image}",
                            "detail" : "high"
                        },
                    },
                ],
            }
        ],
        max_tokens = 300,
    )

    return response.choices[0], message.content
 
#capture_image(0)

""" respuesta = analizar_foto("static/captured_image.jpg")
print(respuesta) """

@app.route("/")
def index():
    cameras = list_cameras()
    return render_template("index.html", cameras=cameras)


@app.route("/capture", methods = ["POST"])
def capture():
    camera_index = int(request.form["camera_index"])
    image_path = capture_image(camera_index)
    if image_path:
        #description = analizar_foto(image_path)
        description = "Sin descripción"
        return render_template("index.html", image_path=image_path, description=description, cameras=list_cameras())
    else:
        return render_template("index.html", error="No se pudo capturar la imagen", cameras=list_cameras())

if __name__ == "__main__":
    app.run(debug=True)
