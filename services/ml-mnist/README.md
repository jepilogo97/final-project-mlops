# Servicio ML - MNIST

Servicio ML para clasificar digitos escritos según el conjunto de datos de referencia MNIST: https://en.wikipedia.org/wiki/MNIST_database

Contenido:
- [Endpoints](#endpoints)
- [Ejecución](#ejecución)
- [Pruebas](#pruebas)
- [Apéndice 1: acceso a objetos de Google Cloud Storage](#apéndice-1-acceso-a-objetos-en-google-cloud-storage)


# Endpoints

El servicio soporta los siguientes endpoints y métodos HTTP:
```
GET /_health

GET /_ready

GET /docs

POST /predict
Content-Type: application/json
{"instances": [IMAGEN_BASE64, IMAGEN_BASE64]}
```

En [src/entities.py](src/entities.py) se encuentran los modelos de solicitud-respuesta para el endpoint `/predict`.


# Ejecución

**Ejecución en local utilizando Docker:**

1. Definir la variable MLMODEL_URI con la ruta del archivo del modelo ONNX:
    ```sh
    # modelo en Google Cloud Storage
    MLMODEL_URI=https://storage.googleapis.com/BUCKET_NAME/PATH/TO/MODEL/mnist_v1.onnx

    # modelo en Google Cloud Storage con acceso privado requiere credenciales (ver apéndice 1)
    MLMODEL_URI=gs://BUCKET_NAME/PATH/TO/MODEL/mnist_v1.onnx
    
    # modelo local a través de servidor de archivos en el directorio de modelos
    # python -m http.server 6060
    # python3 -m http.server 6060

    # el DNS del contenedor apunta `host.docker.internal` al localhost del host de Docker
    MLMODEL_URI=http://host.docker.internal:6060/mnist_v1.onnx
    ```

2. Construir y ejecutar imagen del contenedor:
    ```sh
    # construir imagen
    docker build --target=service -t ml-mnist .

    # ejecutar contenedor en puerto 5000
    docker run --rm --name ml-mnist -e "MLMODEL_URI=${MLMODEL_URI}" -p 5000:80 ml-mnist
    ```

3. Solicitar predicciones declarando instancias:
    ```sh
    IMAGE_PATH=assets/mnist-instance.png
    IMAGE_BASE64=$(base64 -w 0 "$IMAGE_PATH")

    curl -X POST \
        -H 'Content-Type:application/json' \
        -d "{\"instances\": [\"${IMAGE_BASE64}\"] }" \
        localhost:5000/predict
    ```

**Ejecución en local utilizando ambiente virtual:**
1. Configurar ambiente virtual local con `uv` ([https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)):
    ```sh
    # multiplataforma 
    uv sync
    ```

2. Definición de variables de ambiente:
    ```sh
    export ASSETS_DIR=assets/

    export MLMODELS_DIR=

    # modelo local
    export MLMODEL_URI="${MLMODELS_DIR}/mnist_v1.onnx"

    # modelo en Google Cloud Storage
    export MLMODEL_URI=https://storage.googleapis.com/BUCKET_NAME/PATH/TO/MODEL/mnist_v1.onnx

    # modelo en Google Cloud Storage con acceso privado requiere credenciales (ver apéndice 1)
    export MLMODEL_URI=gs://BUCKET_NAME/PATH/TO/MODEL/mnist_v1.onnx
    ```

3. Iniciar servicio:
    ```sh
    # modo producción
    PYTHONPATH=src/ uv run fastapi run src/app.py --port 8000

    # modo desarrollo
    ENVIRONMENT=development PYTHONPATH=src/ uv run fastapi dev src/app.py --port 8000
    ```

3. Solicitar predicciones declarando instancias:
    ```sh
    IMAGE_PATH=assets/mnist-instance.png
    IMAGE_BASE64=$(base64 -w 0 "$IMAGE_PATH")

    curl -X POST \
        -H 'Content-Type:application/json' \
        -d "{\"instances\": [\"${IMAGE_BASE64}\"] }" \
        localhost:8000/predict
    ```


# Apéndice 1: acceso a objetos en Google Cloud Storage

Se requiere asignar credenciales para acceder a objetos en Google Cloud Storage a través de la libería cliente `google-cloud-storage`.
```sh
gcloud auth application-default login
```

Ejecución en local utilizando ambiente virtual donde `google-cloud-storage` automáticamente utiliza las credenciales y lee el proyecto actual de Google Cloud:
```sh
MLMODEL_URI=gs://BUCKET_NAME/PATH/TO/MODEL/mnist_v1.onnx

# modo producción
PYTHONPATH=src/ fastapi run src/app.py --port 8000
```

Ejecución con Docker requiere mapear las credenciales al contenedor y definir el proyecto actual de Google Cloud:
- en Unix (Linux, macOS):
    ```sh
    GOOGLE_CLOUD_PROJECT=
    MLMODEL_URI=gs://BUCKET_NAME/PATH/TO/MODEL/mnist_v1.onnx

    CREDENTIALS="${HOME}/.config/gcloud/application_default_credentials.json"

    docker run --rm --name ml-mnist \
        -e "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
        -e "GOOGLE_APPLICATION_CREDENTIALS=/application_default_credentials.json" \
        -e "MLMODEL_URI=${MLMODEL_URI}" \
        -p 5000:80 \
        -v "${CREDENTIALS}:/application_default_credentials.json:ro" \
        ml-mnist
    ```

- en Windows (PowerShell):
    ```powershell
    $GOOGLE_CLOUD_PROJECT =
    $MLModelUri = "gs://BUCKET_NAME/PATH/TO/MODEL/mnist_v1.onnx"

    $Credentials = "$env:APPDATA\gcloud\application_default_credentials.json"
    
    docker run --rm --name ml-mnist `
        -e "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" `
        -e "GOOGLE_APPLICATION_CREDENTIALS=/application_default_credentials.json" `
        -e "MLMODEL_URI=${MLModelUri}" `
        -p 5000:80 `
        -v "${CREDENTIALS}:/application_default_credentials.json:ro" `
        ml-mnist
    ```

Nota: mapear volúmenes de Docker desde Windows Git-Bash puede resultar en errores de rutas apuntando a "C:/Program Files/Git/", por lo que es preferible utilizar PowerShell.
