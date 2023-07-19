from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

host = os.getenv('db_host')
user = os.getenv('db_user')
password = os.getenv('db_password')
database = 'restaurantData'

mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM restaurantData")
    myresult = mycursor.fetchall()
    for row in myresult:
        print(row[0], row[1], row[2])
    return {"Hello": os.getenv('db_user')}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
