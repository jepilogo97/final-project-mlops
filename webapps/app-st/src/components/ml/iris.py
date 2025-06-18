import json

import httpx
import streamlit as st

from utils.mlservices import get_mlservice_config, request_mlservice


SERVICE_ID = "iris"


def render():   
    svc = get_mlservice_config(SERVICE_ID)
    if len(svc.request_body_samples) == 0:
        value = "{}"
    else:
        value = svc.request_body_samples[0]

    st.subheader("Solicitud JSON")
    request_json = st.text_area("Defina su solicitud JSON:", height=200, value=value)

    response_body = None
    if st.button("Ejecutar"):
        # validar correcta sintaxis del JSON
        try:
            request = json.loads(request_json)
        except json.JSONDecodeError:
            st.error("icesi: invalid JSON in request body.")
            return

        try:
            response_body = request_mlservice(json=request, timeout=10)
        except RuntimeError as e:
            st.error(f"icesi: {e}")
            return

    if response_body is None:
        return

    st.subheader("Respuesta JSON")
    st.json(response_body)
