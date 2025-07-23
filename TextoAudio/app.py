import streamlit as stl
import os
import dotenv as dte
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv(), override=True)

apiKey = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=apiKey)

# Opciones de voz
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

stl.title("Generador de Audio con OpenAI")

text = stl.text_area("Ingrese el texto", height=200)

voice = stl.selectbox("Seleccione la voz:", voices)

# Boton para generar audio
if stl.button("Generar Audio"):
    if text:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        audio_path = "audio.mp3"
        with open(audio_path, "wb") as output_file:
            for chunk in response.iter_bytes():
                if chunk:
                    output_file.write(chunk)

        stl.success("Audio Generado y Guardado en {audio_path}")

        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        stl.audio(audio_bytes, format="audio/mp3")

    else:
        stl.error("Por favor, ingrese un texto.")
