from fastapi import APIRouter, HTTPException
from pydantic  import BaseModel 

router = APIRouter(prefix="/users", tags=["users"], responses={404:  {"message":"No encontrado"}})

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age:int

users_list = [User(id=1, name="Brais", surname="Moure", url="https://moure.dev", age=35),
              User(id=2, name="Moure", surname="Dev",
                   url="https://mouredev.com", age=35),
              User(id=3, name="Brais", surname="Dahlberg", url="https://haakon.com", age=33)]

@router.get("/usersjson")
async def usersjson():  # Creamos un JSON a mano
    return [{"name": "Brais", "surname": "Moure", "url": "https://moure.dev", "age": 35},
            {"name": "Moure", "surname": "Dev",
                "url": "https://mouredev.com", "age": 35},
            {"name": "Haakon", "surname": "Dahlberg", "url": "https://haakon.com", "age": 33}]



@router.get("/")
async def users():
    return users_list

@router.get("/{id}")   #Path
async def user(id:int):
    return search_user(id)

@router.get("/")   #Query
async def user(id:int):
    return search_user(id)

@router.post("/", response_model=User,  status_code=201)
async def user(user: User):
    if type(search_user(user.id))== User:
        raise HTTPException(status_code=404, detail="El usario ya existe")
    users_list.append(user)
    return user
    
@router.put("/", response_model=User, status_code=202)
async def user(user: User):
   
    for index, save_user in enumerate(users_list):
        if save_user.id == user.id:
            users_list[index]= user
            return user
    raise HTTPException(status_code=404, detail="El usario no existe")    
    
@router.delete("/{id}")
async def user(id:int, response_model=User, status_code=202):
   
    for index, save_user in enumerate(users_list):
        if save_user.id == id:
            del users_list[index]
            return "Eliminado"
    raise HTTPException(status_code=404, detail="El usario no existe")    



def search_user(id:int):
    users=filter(lambda user:  user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return "Error: no se encontro el usuario"


