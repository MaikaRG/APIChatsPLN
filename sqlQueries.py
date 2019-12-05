import sqlalchemy
import json
import os
from dotenv import load_dotenv

#class Conection
load_dotenv()
password= os.getenv('password_sql')
engine = sqlalchemy.create_engine('mysql+pymysql://root:{}@localhost/Conversations'.format(password))
conn=engine.connect()

def newUser(newName):
    a = list(conn.execute("SELECT idUser FROM users ORDER BY idUser DESC LIMIT 1"))
    new_userId=a[0][0]+1
    mySql_insert_query="INSERT INTO users (idUser, userName) VALUES ({},'{}')".format(new_userId,newName)
    conn.execute(mySql_insert_query)
    return json.dumps(new_userId)

def listUsers():
    result = list(conn.execute("SELECT * FROM users"))
    return json.dumps([dict(r) for r in result])

def newChat():
    a = list(conn.execute("SELECT idChat FROM chats ORDER BY idChat DESC LIMIT 1"))
    new_chatId=a[0][0]+1
    mySql_insert_query="INSERT INTO chats (idChat) VALUES ({})".format(new_chatId)
    conn.execute(mySql_insert_query)
    return json.dumps(new_chatId)

def chatIdMessages(id_chat):
    mySql_select_query = """SELECT text FROM messages WHERE chats_idchat={}""".format(id_chat)
    a = list(conn.execute(mySql_select_query))
    return json.dumps([dict(r) for r in a])

def listMensUser(user_id):
    mySql_select_query = """SELECT text FROM messages WHERE users_iduser={};""".format(user_id)
    a = list(conn.execute(mySql_select_query))
    return json.dumps([dict(r) for r in a])

def addMessage(chat_id,userid,text):
    mySql_select_query = """select idMessage from messages order by idMessage desc limit 1;"""
    a = list(conn.execute(mySql_select_query))
    idMessage = int(a[0][0]) + 1
    query = """INSERT INTO messages (idMessage, text, datetime, users_iduser, chats_idchat) VALUES ({}, '{}',current_timestamp, {}, {});""".format(idMessage, text, userid, chat_id)
    conn.execute(query)
    return json.dumps(idMessage)

def userAllMessages(user_id):
    query = """SELECT text FROM messages WHERE users_iduser={};""".format(user_id)
    result=list(conn.execute(query))
    return json.dumps([dict(r) for r in result])
