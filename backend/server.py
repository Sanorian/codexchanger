from fastapi import FastAPI
from mysql.connector import connect, Error

app = FastAPI()

@app.get("/")
def getDataAll():
    ...
@app.get("/registration")
def registration(mail: str, nickname: str, password: str):
    ...

@app.get("/login")
def logIn(mail: str, password: str):
    ...

@app.get("/addpost")
def addPost(userID: int, name: str, code: str, language: str, tags: str, publicationDate: str):
    try:
        with connect(
            host="localhost:3306",
            user="root",
            password="root"
        ) as connection:
            with connection.cursor() as cursor:
                getIDRequest = "SELECT ID FROM Programs"
                cursor.execute(getIDRequest)
                for db in cursor:
                    id = (db[len(db)-1]["ID"]) + 1
            request = "INSERT INTO Programs (ID, User_ID, Name, Code, Language, Tags, Publication_date, Moderator_ID, Moderation_Date) VALUES ("+id+", "+userID+", "+name+", "+code+", "+ language+", "+tags+", "+publicationDate+', "", "")'
            with connection.cursor() as cursor:
                cursor.execute(request)
    except Error as e:
        print(e)
