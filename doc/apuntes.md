python manage.py startapp <nombre_de_la_aplicación>

- Crea una nueva aplicación con el nombre que se le indique.
- Crea una nueva aplicación en el directorio actual.
  Esto solo crea el directorio de la aplicación y no agrega ningún archivo de configuración o modelo.
  para hacer que django reconozca la nueva aplicación, se debe agregar el directorio de la aplicación a la variable INSTALLED_APPS en el archivo de configuración de la aplicación.

python manage.py migrate

- Actualiza la base de datos de la aplicación.
- Actualiza la base de datos de la aplicación a la versión más reciente.

python manage.py makemigrations

- Realiza las migracioens de <proyecto>\migrations_initial.py

- Genera un nuevo archivo de migración para la aplicación.
- Genera un nuevo archivo de migración para la aplicación en el directorio actual.

python manage.py runserver

- Sirve para ejecutar el servidor de desarrollo de la aplicación
- El servidor de desarrollo es una aplicación web que se ejecuta en el puerto 8000 de la máquina local.
- El servidor de desarrollo se ejecuta en modo de desarrollo, lo que significa que se ejecutará en modo de desarrollo y no en modo de producción.

# Arquitectura de la aplicación

- proyecto con django
  - aplicación conexion
