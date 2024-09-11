from fastapi import APIRouter, Depends, HTTPException, status
from pydantic  import BaseModel 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2= OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password:str


users_db= {
    "Diego": {   
        "username": "Diego",
        "full_name": "Diego Masip",
        "email": "arie@gmail.com",
        "disabled": False,
        "password": "123456"
    },

    "Diego2": {   
        "username": "Diego2",
        "full_name": "Diego Masip2",
        "email": "arie2@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}

def search_user(username:str):
    if username in users_db:
        return  User(**users_db[username])

def search_user_db(username:str):
    if username in users_db:
        return  UserDB(**users_db[username])
    
async def current_user(token: str=Depends(oauth2)):
    user= search_user(token)
    if not user:
         raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                             detail="Credenciales de autenticación invalidda",
                             headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
        user_db= users_db.get(form.username )
        if not user_db:
             raise HTTPException(status_code=400, detail="El usario no existe")
        
        user=search_user_db(form.username)
        if not user.password == form.password:
             raise HTTPException(status_code=400, detail="La contraeña es incorrecta")
        
        return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User= Depends(current_user)):
    return user

