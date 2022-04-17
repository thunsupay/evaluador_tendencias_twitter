# evaluador_tendencias_twitter
Herramienta en Python que permite evaluar tendencias de Twitter.

El aplicativo requiere un archivo con las variables de entorno, las variables de entorno deben quedar de la siguiente forma:
```sh
bearer_token=<twitter_bearer_token>
consumer_key=<twitter_consumer_key>
consumer_secret=<twitter_consumer_secret>
access_token=
access_token_secret=
wait_on_rate_limit=true
```
La ruta de ubicación del archivo para el ejemplo debe estar en:

./main/project/.env


## 1. Instalación del entorno virtual
CMD
```sh
pip install virtualenv
```

## 2. Creación del módulo virtual
CMD
```sh
python -m virtualenv main
python -m venv main
```

## 3. Activar entorno virtual
CMD
```sh
./main/Scripts/activate
```

## 4. Verificación e installación de librerías en el entorno virtual
El listado de paquetes necesarios se encuentra en el archivo requirements.txt.
```sh
pip install -r requirements.txt
```
Se puede verificar que los paquetes están instalados ejecutar el siguiente comando:
```sh
pip freeze
```

## 5. Generación de la base de datos
CMD
```sh
./main/Scripts/python.exe ./main/project/db/generateTables.py
```

## 6. Ejecución del aplicativo
CMD
```sh
./main/Scripts/python.exe ./main/project/main.py
```

## 7. Desactivar entorno virtual
CMD
```sh
deactivate
```