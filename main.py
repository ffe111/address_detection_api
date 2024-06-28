from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from thaiAddressTag.tag import *
from thaiAddressTag.hashmaps import hashmap
from thaiAddressTag.addresses import address_list

# import thaiaddress

custom_tokenize, checker = initial_nlp_tools(hashmap)

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Text(BaseModel):
    text: str


@app.get("/")
def read_root() -> Union[str, int]:
    return "Welcome to address-check API\nUse path /address-check to check address\nUse path /docs to see API documentation\nUse path /redoc to see API documentation\n"


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None) -> dict:
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


@app.post("/address-check")
def address_check(text: Text) -> dict:
    text = text.text
    res = extract_address(text, custom_tokenize=custom_tokenize,
                          checker=checker, address_list=address_list)
    return {"address": res}


# @app.post("/address-parser")
# def address_parser(text: Text) -> dict:
#     text = text.text
#     res = thaiaddress.parse(text)
#     return {"address": res}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="info")
