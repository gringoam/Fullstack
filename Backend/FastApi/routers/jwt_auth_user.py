from fastapi import APIRouter, Depends, HTTPException, status
from pydantic  import BaseModel 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

ALGORITHM="HS256"
ACCES_TOKEN_DURATION=1
SECRET= "7d6e47a632c98a9f0de2227ab097e100511c83a4a2dbdcb608fb30ef1c4b9c88"

oauth2= OAuth2PasswordBearer(tokenUrl="login")
crypt= CryptContext(schemes=["bcrypt"])

ALGORITHM="HS256"
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
        "password": "$2a$12$ZfeS4JPMNmJXJsaROiLBYuOUwrtIIFmgKRH7JyKUffeiQbzupta32"
    },

    "Diego2": {   
        "username": "Diego2",
        "full_name": "Diego Masip2",
        "email": "arie2@gmail.com",
        "disabled": True,
        "password": "$2a$12$IB1QH5zIcHDJ7VKigZwm/.Yd2rRTkozXbL3Hh9mSvJObiEozT9k9e"
    }
}

def search_user_db(username:str):
    if username in users_db:
        return  UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return  User(**users_db[username])
    
async def auth_user(token:str=Depends(oauth2)):
    

    exception=HTTPException(status.HTTP_401_UNAUTHORIZED,
                             detail="Credenciales de autenticación invalidda",
                             headers={"WWW-Authenticate": "Bearer"})
    try:
        username= jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if  username is None: 
             raise exception
             
    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: str=Depends(auth_user)):
    
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
        if not crypt.verify(form.password, user.password):
             raise HTTPException(status_code=400, detail="La contraeña es incorrecta")
        
    
        
        acces_token={"sub": user.username,
                     "exp": datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)
                    }

        return {"access_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User= Depends(current_user)):
    return user
    