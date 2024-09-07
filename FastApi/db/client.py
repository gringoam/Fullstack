from pymongo import MongoClient             

#Baase de datos local
#db_client= MongoClient().local 

db_client= MongoClient("mongodb+srv://FastApi:griclafastapi@cluster0.hiu5o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").fastapi