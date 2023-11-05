from fastapi import FastAPI
from mysql.connector import connect, Error

app = FastAPI()

# для получения всех постов
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
                    id = int(db[len(db)-1]["ID"]) + 1
            request = "INSERT INTO Programs (ID, User_ID, Name, Code, Language, Tags, Publication_date, Moderator_ID, Moderation_Date) VALUES ("+id+", "+userID+", "+name+", "+code+", "+ language+", "+tags+", "+publicationDate+', "", "")'
            with connection.cursor() as cursor:
                cursor.execute(request)
                return {"res": "good"}
    except Error as e:
        print(e)
        return {"res": "bad"}

@app.get("/getposts")
def getPosts(search: str, language: str, tags: str):
    try:
        with connect(
            host="localhost:3306",
            user="root",
            password="root"
        ) as connection:
            if language and search and tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE code LIKE '%"+search+"% AND WHERE Language='"+language+"'"
                for tag in tags.split(" "):
                    request += " AND WHERE code LIKE '%"+tag+"%'"         
            elif language and search:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE code LIKE '%"+search+"% AND WHERE Language='"+language+"'"
            elif language and tags:
                request = 'SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE Language="'+language+'"'
                for tag in tags.split(" "):
                    request += " AND WHERE code LIKE '%"+tag+"%'"           
            elif search and tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE code LIKE '%"+search+"%'"
                for tag in tags.split(" "):
                    request += " AND WHERE code LIKE '%"+tag+"%'"
            elif language:
                request = 'SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE Language="'+language+'"'
            elif search:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE code LIKE '%"+search+"%'"
            elif tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs"
                for tag in tags.split(" "):
                    request += " AND WHERE code LIKE '%"+tag+"%'"           
            with connection.cursor() as cursor:
                cursor.execute(request)
                for db in cursor:
                    return db
    except Error as e:
        print(e)
        return {"res": "bad"}