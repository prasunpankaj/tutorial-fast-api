# import uvicorn
from datetime import date
from typing import Optional
from enum import Enum
from xmlrpc.client import DateTime
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
    tax: Optional[float] = None
    
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
    
# Declare a variable as a str
# and get editor support inside the function    
def main(user_id: str):
    return user_id

# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date

@app.get("/")
async def read_root():
    return "Hello World"


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/items")
async def read_itme(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.post("/items/")
async def create_item(item: Item):
    item_dect = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dect.update({"price_with_tax": price_with_tax})
        item_dect.update({"final_output": price_with_tax-10})
    return item_dect

@app.post("/users/")
async def create_user(user: User):
    user_dect = user.dict()
    if user.name:
        #DB Saving will do
        user.joined = DateTime
    return user_dect

def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

@app.get("/names/")
async def append_name(first_name: str, last_name: str):
    full_name = get_full_name(first_name, last_name)
    print(full_name)
    name_dict = {"full_name": full_name}
    return name_dict
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)