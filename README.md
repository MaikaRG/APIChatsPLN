# APIChatsPLN

https://apisentiment.herokuapp.com/

En esta API podrás consultar:

    - @get("/"):
    Estado : 'Conectado'

    - @get('/users'):
    Lista de Usuarios en la BDD.

    - @get('/chat/<id_chat>/list'):
    Devuelve los mensajes del chat seleccionado

    - @get("/user/<user_id>/messages"):
    Devuelve una lista de mensajes por usuario (el seleccionado)

    - @get('/user/<user_id>/sentiment')
    Devuelve la media de los sentimientos por usuario en función a sus mensajes

    - @get('/chat/<chat_id>/sentiment'):
    Devuelve la media de los sentimiento en el chat seleccionado

    - @get("/user/<user_id>/messages"):
    Devuelve todos los mensajes de el usuario seleccionado

    - @get('/user/<user_id>/recomend'):
    Devuelve 3 recomendaciones por usuario seleccionado de los usuarios que tienen en común de lo que hablan.

En esta API podrás añadir:

    - @post('/user/create')
    Puedes introducir el nombre de un usuario, haciendo una requests.post(), 
    {'newName'}:{'X'}

    - @post('/chat/create')
    Crea un nuevo chat al hacer una requests.post

    - @post('/chat/<chat_id>/addmessage')
    Puedes intruducir:
    {'userid': int, 'message':'X'}
    Se añadira el mensaje de ese usuario al chat elegido