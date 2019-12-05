import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlQueries
import sqlalchemy
import numpy as np
import json
import os
from dotenv import load_dotenv

load_dotenv()
password= os.getenv('password_sql')
engine = sqlalchemy.create_engine('mysql+pymysql://root:{}@localhost/Conversations'.format(password))
conn=engine.connect()

def mensajesusuario(user_id):
    mySql_select_query = """SELECT text FROM messages WHERE users_iduser={};""".format(user_id)
    a = list(conn.execute(mySql_select_query))
    sid = SentimentIntensityAnalyzer()
    lista=[]
    for e in a:
        s = sid.polarity_scores(str(e))
        lista.append(s)
    return json.dumps([dict(r) for r in lista])

def mensajesChat(chat_id):
    mySql_select_query = """SELECT text FROM messages WHERE chats_idChat={};""".format(chat_id)
    a = list(conn.execute(mySql_select_query))
    sid = SentimentIntensityAnalyzer()
    lista=[]
    for e in a:
        s = sid.polarity_scores(str(e))
        lista.append(s)
    return json.dumps([dict(r) for r in lista])


def mediaSentimientos(user_id):
    lista=[]
    for e in json.loads(mensajesusuario(user_id)):
        lista.append(e)
    negatividad = np.mean([v for e in lista for k,v in e.items() if k == 'neg'])
    neutralidad = np.mean([v for e in lista for k,v in e.items() if k == 'neu'])
    positividad = np.mean([v for e in lista for k,v in e.items() if k == 'pos'])
    composicion = np.mean([v for e in lista for k,v in e.items() if k == 'compound'])
    return {'negatividad':negatividad,'neutralidad':neutralidad,'positividad':positividad,'composicion':composicion}


def mediaSentimientosChat(chat_id):
    lista=[]
    for e in json.loads(mensajesChat(chat_id)):
        lista.append(e)
    negatividad = np.mean([v for e in lista for k,v in e.items() if k == 'neg'])
    neutralidad = np.mean([v for e in lista for k,v in e.items() if k == 'neu'])
    positividad = np.mean([v for e in lista for k,v in e.items() if k == 'pos'])
    composicion = np.mean([v for e in lista for k,v in e.items() if k == 'compound'])
    return {'negatividad':negatividad,'neutralidad':neutralidad,'positividad':positividad,'composicion':composicion}
