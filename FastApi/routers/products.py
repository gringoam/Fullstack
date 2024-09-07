from fastapi import APIRouter, HTTPException
from pydantic  import BaseModel 

router = APIRouter(prefix="/products", tags=["products"], responses={404:  {"message":"No encontrado"}})

products_list=["productos 1", "producto 2", "producto 3", "producto 4", "producto 5"]

@router.get("/")   
async def product():
    return products_list

@router.get("/{id}")   #Path
async def product(id:int):
    return products_list[id]