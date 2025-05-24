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

Los pasos son casi iguales, solo cambia la forma de activar el entorno virtual (venv).

    El entorno virtual se encuentra en la carpeta venv, y dentro de ella está la carpeta bin con los ejecutables .sh.

    Para activar el entorno virtual, ejecuta en la terminal:

source venv/bin/activate

En caso de que no uses terminales comunes (como bash o zsh), y por ejemplo uses fish, deberás indicarlo así:

source venv/bin/activate.fish

Por último, para correr el servidor y acceder a la página web:

    python manage.py runserver

Y listo, ¡creo que eso es todo lo que necesitas saber! :v
