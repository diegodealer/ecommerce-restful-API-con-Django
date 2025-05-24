Proyecto E-commerce con RESTful API en Django

Este proyecto fue realizado para una materia que se me pidió, aunque es bastante interesante si quieres adentrarte en el mundo de las RESTful API o aprender Django. Así que eres libre de revisar este proyecto.

En caso de que quieras probarlo, es importante que sepas que puede usarse tanto en Windows como en Linux.
Instrucciones para Windows:

    Tener instalado Python 3.11 o superior, junto con su gestor de paquetes llamado pip (esto debería ser muy obvio, pero tengo mis dudas).

    Tener Django instalado en tu computadora.
    Si no sabes cómo configurarlo, visita el sitio oficial y consulta la documentación:
    https://www.djangoproject.com/
    Ahí te explican paso a paso cómo instalarlo y configurarlo.

    Una vez que clones el repositorio, verás una carpeta llamada Scripts/.

    Para activar el entorno virtual, usa el siguiente comando en la terminal:

venv\Scripts\activate

Al ejecutarlo, el entorno virtual se activará automáticamente.

En caso de error, podría deberse a que el proyecto admite la inserción de imágenes, por lo que deberás instalar Pillow con el siguiente comando:

pip install Pillow

Por último, para correr el servidor y acceder al sitio web, ejecuta:

    python manage.py runserver

    Este comando te dará la IP local para acceder al proyecto, y se abrirá en tu navegador predeterminado.

Instrucciones para Linux:

Los pasos son casi iguales, solo cambia la forma de activar el entorno virtual.

Importante: El entorno virtual (venv) no está incluido en el repositorio, por lo que debes crearlo tú mismo en Linux siguiendo estos pasos:

    Abre la terminal y navega a la carpeta raíz del proyecto (donde está manage.py).

    Crea el entorno virtual con el siguiente comando:

python3 -m venv venv

Activa el entorno virtual:

    Si usas una terminal estándar (bash, zsh):

source venv/bin/activate

Si usas fish shell:

    source venv/bin/activate.fish

Una vez activado el entorno virtual, instala las dependencias necesarias (incluyendo Django y Pillow, si no las tienes instaladas):

pip install -r requirements.txt

Si no tienes un archivo requirements.txt, instala Django y Pillow manualmente:

pip install django pillow

Para correr el servidor y acceder a la página web, ejecuta:

    python manage.py runserver

¡Y listo! Así podrás usar el proyecto en Linux sin problemas.
