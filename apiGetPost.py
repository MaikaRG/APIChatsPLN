from bottle import request, response
from bottle import route, run, get, post
import sqlQueries
import sqlalchemy
import json
import sentiment
import os
from dotenv import load_dotenv
import recomendaciones
#from mongo import CollConection

@get("/")
def index():
    return 'Conectado'

@post('/user/create')
def addNewUser():
    newName = str(request.forms.get("newName"))
    print(newName)
    return sqlQueries.newUser(newName)

@get('/users')
def usersAll():
    return sqlQueries.listUsers()

@post('/chat/create')
def addChat():
    return sqlQueries.newChat()

@get('/chat/<id_chat>/list')
def chatIdMessages(id_chat):
    return sqlQueries.chatIdMessages(id_chat)

@get("/user/<user_id>/messages")
def userMessages(user_id):
    return sqlQueries.listMensUser(user_id)

@post('/chat/<chat_id>/addmessage')
def newMess(chat_id):
    userid = int(request.forms.get("userid"))
    text = str(request.forms.get("message"))
    return sqlQueries.addMessage(chat_id,userid,text)

@get('/user/<user_id>/sentiment')
def sentimentUser(user_id):
    return sentiment.mediaSentimientos(user_id)

@get('/chat/<chat_id>/sentiment')
def sentimentChar(chat_id):
    return sentiment.mediaSentimientosChat(chat_id)

@get("/user/<user_id>/messages")
def userMessages(user_id):
    return sqlQueries.userAllMessages(user_id)

@get('/user/<user_id>/recomend')
def recomendacion(user_id):
    return recomendaciones.userRecommend(user_id)

load_dotenv()
password= os.getenv('password_sql')
engine = sqlalchemy.create_engine('mysql+pymysql://root:{}@localhost/Conversations'.format(password))
conn=engine.connect()
run(host='0.0.0.0', port=8080)

# port = int(os.getenv("PORT", 80))
# print(f"Running server {port}....")

# run(host="0.0.0.0", port=port, debug=True)
