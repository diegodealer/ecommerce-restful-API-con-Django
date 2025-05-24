Proyecto e-commerce CON restful API Django


Este proyecto fue hecho para una materia que se me pidio, aunque es bastante interesante si quieres entrar al mundo de las restful-apui 
o quieres aprender Django, asi que eres libre de ver este proyecto. 

En caso de que quieras probarlo es importante que sepas que e puede usar tanto en windows como en linux 
para windows tienes que:

- tener instalado pytjon 3.11 en delante con su gestor de paquetes llamado pip (esto debe ser muy obvio pero tengo mis dudas)

- tener Djhango instalado en tu computadora (si no sabes como configurarlo ve al sitio web oficial y consulta la documentacion https://www.djangoproject.com/,
alli te diran paso a paso como instalarlo y configurarlo).

- si ya tienes Django instalado  cuando clones el repositorio veras una carpeta llamada Scripts/

- asi que si tienes para activarlo usaras el siguiente directorio "venv\Scripts\activate"
con dar click se activara automaticamente el entorno virtual

- en caso de algun error tambien se podria deber a que el proyecto soporta insercion de imagenes por lo que tendras que instalar pillow
utilizando el siguiente comando "pip install Pillow".

- por ultimo para correr el servidor y acceder a la pagina web y todo el proyecto deberas poner este comando en la terminal
- "python manage.py runserver"

- ese comando te dara la ip para acceder y se abrira en tu navegador de preferencia.

Ahora para linux son casi iguales los comandos solamente que en el venv (entorno virtual) la cosa es diferente

- en este caso el entorno virtual para usar el proyecto con linux es la carpeta "venv" dentro de ella estara la carpeta bin con los ejecutables .sh

- para activar el venv entonces deberas poner lo siguiente en la terminal "source venv/bin/activate"

- en caso de que no uses las terminales comunes y por ejemplo uses fish debes señalarlo al final de la ruta
- "source venv/bin/activate.fish"

- por ultimo para correr el servidor y acceder a la pagina web: "python manage.py runserver"

y listo creo que es todo lo que necesitas saber :v
