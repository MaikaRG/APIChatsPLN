from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np
import json
import sqlQueries
import sqlalchemy
import json
import os
from dotenv import load_dotenv

# url=os.getenv("DATABASE_URL",'postgres://ksbeewuctebulz:12e8ca1d78c8f71110e63556927bf3ca5894db2ccfc7766528139906f114e520@ec2-54-217-221-21.eu-west-1.compute.amazonaws.com:5432/d6n20g4sij6qdp')
# engine = sqlalchemy.create_engine(url)
load_dotenv()
password= os.getenv('password_sql')
engine = sqlalchemy.create_engine('mysql+pymysql://root:{}@localhost/Conversations'.format(password))
conn=engine.connect()


def userRecommend(user_id):
    query = """select userName from users where idUser={}""".format(user_id)
    a = list(conn.execute(query))
    name = json.dumps(a[0][0])
    name = name.strip('"')
    a = sqlQueries.listUsers()
    data = json.loads(a)
    docs = dict()
    listaDic=[]
    for i in data:
        listaDic.append(dict(i))
    for u in listaDic:
        #print(u)
        messages = sqlQueries.userAllMessages(u['idUser'])
        #print(messages)
        docs.update({u['userName']:(messages)})
    # Create the Document Term Matrix
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(docs.values())
    # Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=docs.keys())
    # Compute Cosine Similarity matrix (or selected distance)
    similarity_matrix = distance(df, df)
    sim_df = pd.DataFrame(similarity_matrix, columns=docs.keys(), index=docs.keys())
    # Remove diagonal max values and set those to 0
    np.fill_diagonal(sim_df.values, 0)
    res = {'recommended_users': [e for e in list(sim_df[name].sort_values(ascending=False)[0:3].index)]}
    return res