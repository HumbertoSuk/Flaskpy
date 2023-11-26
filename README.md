# Nombre del Proyecto

La tienda de cafetería es un proyecto web diseñado para ofrecer a los usuarios una experiencia completa al explorar y comprar productos en línea desde la comodidad de sus dispositivos. Desarrollado con tecnologías como Flask, HTML, CSS y JavaScript, esta aplicación combina funcionalidad y estética para crear un entorno atractivo y fácil de usar.

La interfaz de usuario, construida con HTML y CSS, presenta un diseño limpio y moderno que refleja la esencia acogedora y reconfortante de una cafetería. El enfoque en la responsividad garantiza una experiencia uniforme en una variedad de dispositivos, desde computadoras de escritorio hasta tablets y teléfonos móviles, permitiendo a los usuarios explorar el catálogo de productos de manera fluida y eficiente.

La funcionalidad principal del sitio web se implementa mediante Flask, un marco web de Python que facilita el desarrollo rápido y eficiente de aplicaciones web. Flask gestiona las operaciones del lado del servidor, asegurando una comunicación eficiente entre el cliente y la base de datos. La arquitectura modular de Flask permite una fácil expansión de características, proporcionando una base sólida para futuras mejoras y actualizaciones.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

- Python 
- MySQL
- Flask

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/HumbertoSuk/Flaskpy.git
    ```

2. Ve al directorio del proyecto:

    ```bash
    cd /Directorio de instalacion
    ```

3. Crea y activa un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate      # Para sistemas basados en Unix
    # o
    .\venv\Scripts\activate       # Para sistemas basados en Windows
    ```

4. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

5. Configura la base de datos:

    - Crea una base de datos MySQL.
    - Actualiza la configuración de la base de datos en el archivo `config.py`.
    - ejecutar los scripts en la BD o importa la BD  en la carpeta de BD
  

   ``` Bash
   
    pip install -r requirements.txt


   ```

6. Ejecuta la aplicación:

``` bash
class DevelopmentConfig():
    DEBUG = True
    SECRET_KEY = "qhrf$edjYTJ)*21nsThdK"
    MYSQL_HOST = "localhost" //Cambiar el host
    MYSQL_USER = "root" //Cambiuar el usuario
    MYSQL_PASSWORD = "Fidelio1524" //Contraseña
    MYSQL_DB = "store" 


config = {"development": DevelopmentConfig}

```

7. Accede a la aplicación desde tu navegador:

   Ejecutar el app.py

   ```bash
   python ./src/app.py

   ```

Accede a la aplicacion

   `http://127.0.0.1:5000/`

## Uso

Explora el Catálogo:

- 1 `Iniciar sesion:`  en el campo Usuario y Contraseña poner los correspondientes del usuario, si no se tiene por default es el usuario Admin y contra 123.
     - Si no coinciden te mandara un error. 

Desde la página del producto, haz clic en el botón "Agregar al Carrito".
Visita tu carrito para revisar los productos seleccionados.
Proceso de Compra:

En la página del carrito, haz clic en "Comprar Ahora" para iniciar el proceso de compra.
Completa la información requerida para la compra.
Finalización de la Compra:

Revisa y confirma tu compra.
¡Felicidades! Has completado con éxito una compra en la Tienda de Cafetería.

## Contribuciones

Este proyecto se hizo bajo la colaboracion de Kevin Fausto estudiante de Ing. en sistemas computacionales.


