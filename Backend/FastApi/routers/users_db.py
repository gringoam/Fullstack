from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb", tags=["userdb"], responses={404:  {"message":"No encontrado"}})





@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}")   #Path
async def user(id:str):
    return search_user("_id", ObjectId(id))

@router.get("/")   #Query
async def user(id:str):
    return search_user("_id", ObjectId(id))

@router.post("/", response_model=User,  status_code=status.HTTP_201_CREATED)
async def user(user: User):
    
   
    if type(search_user("email", user.email))== User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usario ya existe")
    
    
    user_dict=dict(user)
    print(user_dict)
    id= db_client.users.insert_one(user_dict).inserted_id

   
    #del user_dict["id"]
    new_user= user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", response_model=User, status_code=202)
async def user(user: User):
    user_dict= dict(user)
    del user_dict["id"]
    print(user_dict)
    try:
       db_client.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: No se a actualizado el usuario")
    
    return search_user("_id", ObjectId(user.id))  
    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str ):
   
   found= db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    
   if not found:
           return {"No se a eliminado el usuario"}



def search_user(field:str, key):
    
    try:
        user=db_client.users.find_one({field:key})
        return User(**user_schema(user)) 
    
    except:
        return "Error: no se encontro el usuario"
    
