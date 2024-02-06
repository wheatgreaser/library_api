from fastapi import FastAPI, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
   

my_posts = [{"title": "Cool beaches in Miami", "content": "wait bondi beach is in sydney?", "id" : 1},
            {"title": "top pizza shops in New York", "content" : "Uncle Joes", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_posts(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i



@app.get("/")
def root():
    return {"message": "its aping time"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM postdata""")
    coolposts = cursor.fetchall()
    return{"data" : coolposts}

@app.post("/posts")
def create_posts(post: Post):
    cursor.execute("""INSERT INTO postdata (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data" : new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM postdata WHERE id = (%s)""", (str(id)))
    post = cursor.fetchone()
    conn.commit()
    return{"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int, response: Response):
    cursor.execute("""DELETE FROM postdata WHERE id = (%s)""", (str(id)))
    conn.commit()
    return{"message": "post deleted"}
   

@app.put("/posts/{id}")
def update_post(id:int, post: Post, response: Response):
    cursor.execute("""UPDATE postdata SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    return{"message": post}

while(True):
    try:
        conn = psycopg2.connect()
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:

        print("connection to database failed")
        print("Error: ", error)
        time.sleep(2)


    
