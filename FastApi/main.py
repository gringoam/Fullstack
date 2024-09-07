from fastapi import FastAPI
from routers import users, products, basic_auth_user, jwt_auth_user, users_db
from  fastapi.staticfiles import StaticFiles
 

app = FastAPI()

#Routers
app.include_router(users.router)
app.include_router(users_db.router)
app.include_router(products.router)
app.include_router(basic_auth_user.router)
app.include_router(jwt_auth_user.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"Hola fastApis"}

"""@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}"""



