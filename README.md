# gmeBox

# REQUIREMIENTOS

- Instalar python 3.6
- Instalar pip
- Instalar mysql>5.7
- Instalar virtualenv
- Crear entorno virtual
  `virtualenv -p python3.6 /path/gmeBoxEnv`
- Instalar librerias para ello de debe ubicar en la raiz del proyecto a la altura del archivo `manage.py` y colocar el comando `pip3 install -r requirements.txt` o `pip install -r requirements.txt`
- Crear una base de datos en mysql llamada `gmebox`
- Correr el comando `python manage.py migrate`</br>
- Crear super usuario `python manage.py shell`</br>
- Escribir el siguiente comando
  from people.models import Usuario</br>
  usuario = Usuario.objects.create_superuser(email='dlinahuazo@tecnologicosudamericano.edu.ec', password='gmeBox', username='dlinahuazo')

# Documentación

- Para ver la documentación del proyecto la aplicación se debe ir a la ruta `{IP}:{PUERTO}/admin/doc/` aqui un ejemplo
  `http:localhost:8000/admin/doc/` y se podrá observar toda la documentación de los modelos, vistas, admin, formularios y urls
