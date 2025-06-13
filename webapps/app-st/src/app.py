import streamlit as st

import components.mlmodels_selector as mlmodel_selection
import components.ml as mlcomponents
from utils.states import get_app_state_mapping, get_mlmodel_type_state_kv, map_session_state


if 'app' not in st.session_state:
    st.session_state['app'] = True
    map_session_state(get_app_state_mapping())


def render():
    st.title("Interacción con modelos MLOps")

    mlmodel_selection.render()
    (_, mlmodel_type) = get_mlmodel_type_state_kv()
    if mlmodel_type == "":
        return

    try:
        mlcomponent = getattr(mlcomponents, mlmodel_type)
    except AttributeError:
        st.error(f"icesi: no se encontró el componente para el tipo de modelo: {mlmodel_type}")
        return
    except Exception as e:
        st.error(f"icesi: error cargando el componente del modelo: {mlmodel_type}: {e}")
        return

    mlcomponent.render()


render()
