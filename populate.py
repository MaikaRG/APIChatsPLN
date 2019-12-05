import os
import json
import sqlalchemy

url=os.getenv("DATABASE_URL",'postgres://vsxgpacxlqqvux:ab801cb02e34af049aa703f9493177e756823cd9574a24295a1e67fc5037ee3b@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dffsm2m59k3jl7')
#DATABASE_URL = 'localhost:3306'
#Connect to DB
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#"mysql://u:p@host/db"
engine = sqlalchemy.create_engine(url)
#If permission Error
#conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

#Create Cursor
#cur = conn.cursor()
#Create Tables
query = query = """
CREATE TABLE IF NOT EXISTS users (
  idUser INT NOT NULL, 
  userName VARCHAR(45) NOT NULL,
  PRIMARY KEY (idUser));
CREATE TABLE IF NOT EXISTS chats (
  idChat INT NOT NULL,
  PRIMARY KEY (idChat));
CREATE TABLE IF NOT EXISTS messages (
  idMessage INT NOT NULL,
  text VARCHAR(120) NULL,
  datetime VARCHAR(45) NULL,
  users_idUser INT NOT NULL,
  chats_idChat INT NOT NULL,
  PRIMARY KEY (idMessage),
    FOREIGN KEY (users_idUser)
    REFERENCES users (idUser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Message_chats1
    FOREIGN KEY (chats_idChat)
    REFERENCES chats (idChat)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)"""


with engine.connect() as conn:
  conn.execute(query)
print("Database created.")

#Populate Tables

query = "INSERT INTO {} VALUES {}"


with open('chats.json') as f:
    chats_json = json.load(f)


users = list(set([(chats_json[i]['idUser'],chats_json[i]['userName']) for i in range(len(chats_json))]))
print(users)
chats = list(set([(chats_json[i]['idChat']) for i in range(len(chats_json))]))
for user in users:
  q = query.format('users (idUser, userName)',"({}, '{}')".format(user[0],user[1]))
  print(q)
  with engine.connect() as conn:
    conn.execute(q)
  #Get Response
  #id = conn.fetchone()[0]
  print("value inserted")
  
for chat in chats:
  q = query.format('chats(idChat)',"({})".format(chat),'chats.idChat')
  print(q)
  try:
    with engine.connect() as conn:
      conn.execute(q)
    #Get Response
    #id = conn.fetchone()[0]
    print("value inserted")
  except:
    print("At least I tried")

for message in chats_json:
  q = query.format('messages(idMessage, text, datetime, users_idUser, chats_idChat)',"({},'{}','{}',{},{})".format(message['idMessage'],message['text'],message['datetime'],message['idUser'],message['idChat'],),'messages.idMessage')
  print(q)
  try:
    with engine.connect() as conn:
      conn.execute(q)
    #Get Response
    #id = conn.fetchone()[0]
    print("value inserted")
  except:
    print("At least I tried")
    
print('Done!')
