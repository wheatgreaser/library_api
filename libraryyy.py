from fastapi import FastAPI, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

books = [{"name": "Kafka on the shore", "genre":"idfk", "author":"murakami", "id":1}, {"name": "harry potter", "genre":"fantasy", "author":"just kidding rolling", "id":2}]

class Book(BaseModel):
    name: str
    genre: str
    author: str
    id: int

def get_book(id):
    for b in books:
        if(b["id"] == id):
            return b

@app.get("/books")
def get_all_books():
    return{"message": books}

@app.get("/book/{id}")
def get_a_book(id: int, response:Response):  
    selected_book = get_book(id)
    if(selected_book == None):
        response.status_code = 404
        return{"message": "book not found"}
    return{"message": selected_book}

@app.post("/book")
def add_a_book(newbook: Book):
    bookified = newbook.dict()
    books.append(bookified)
    return{"message": bookified}

