import base64
import io
import json

import httpx
import streamlit as st
import streamlit.components.v1 as components

from PIL import Image

from components.custom import render_custom_component
from utils.mlservices import request_mlservice


SERVICE_ID = "mnist"


def render_demo():
    try:
        response = request_mlservice(resource_path="/predict-demo", timeout=10)
    except RuntimeError as e:
        st.error(f"icesi: {e}")
        return

    image_bytes = base64.b64decode(response["source_demo_image_base64"])
    image_source = Image.open(io.BytesIO(image_bytes))
    del response["source_demo_image_base64"]

    st.image(image_source, caption="Imagen utilizada en el demo del servicio de predicción", width=150)
    st.subheader("Respuesta JSON")
    st.json(response)


def render_predict_image_base64(image_base64: str):
    # preprocesar imagen para reducir tamaño de solicitud a servicio ML
    image_bytes = base64.b64decode(image_base64)
    image_procesed = Image.open(io.BytesIO(image_bytes)).convert("L").resize((28, 28))

    # codificar imagen en base64 para solicitud a servicio ML
    buffered = io.BytesIO()
    image_procesed.save(buffered, format="PNG")
    image_procesed_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    try:
        request = {"instances": [image_procesed_base64]}
        response = request_mlservice(json=request, timeout=10)
    except RuntimeError as e:
        st.error(f"icesi: {e}")
        return

    st.image(image_procesed, caption="Imagen enviada al servicio de predicción", width=150)
    st.subheader("Respuesta JSON")
    st.json(response)


def render():
    st.subheader("Dibuje un número")
    drawing_json = render_custom_component("canvas", key="my_unique_key")

    if st.button("Ejecutar demo"):
        render_demo()
    elif drawing_json:
        try:
            drawing = json.loads(drawing_json)
        except json.JSONDecodeError:
            st.error("icesi: error decoding drawing JSON value from canvas custom component")
            return

        render_predict_image_base64(drawing["image_base64"])
