from fastapi import FastAPI
from mysql.connector import connect, Error

app = FastAPI()

#Получение всех постов, но без Moderator_id, Moderation_time и code
@app.get("/")
def getDataAll():
    ...

#Регистрация
@app.get("/registration")
def registration(mail: str, nickname: str, password: str):
    ...

#Вход
@app.get("/login")
def logIn(mail: str, password: str):
    ...

#Добавление постов
@app.get("/addpost")
def addPost(userID: int, name: str, code: str, language: str, tags: str, publicationdate: str):
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
            request = "INSERT INTO Programs (ID, User_ID, Name, Code, Language, Tags, Publication_date, Moderator_ID, Moderation_Date) VALUES ("+id+", "+userID+", "+name+", "+code+", "+ language+", "+tags+", "+publicationdate+', "", "")'
            with connection.cursor() as cursor:
                cursor.execute(request)
                return {"res": "good"}
    except Error as e:
        print(e)
        return {"res": "bad"}

#Получение постов с условием
@app.get("/getposts")
def getPosts(search: str | None = None, language: str | None = None, tags: str | None = None):
    try:
        with connect(
            host="localhost:3306",
            user="root",
            password="root"
        ) as connection:
            if language and search and tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE NOT Moderator_ID = '' AND WHERE NOT Moderation_date = '' AND WHERE code LIKE '%"+search+"% AND WHERE Language='"+language+"'"
                for tag in tags.split(" "):
                    request += " AND WHERE code LIKE '%"+tag+"%'"         
            elif language and search:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE NOT Moderator_ID = '' AND WHERE NOT Moderation_date = '' AND WHERE code LIKE '%"+search+"% AND WHERE Language='"+language+"'"
            elif language and tags:
                request = 'SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE NOT Moderator_ID = '' AND WHERE NOT Moderation_date = '' AND WHERE Language="'+language+'"'
                for tag in tags.split(" "):
                    request += " AND WHERE code LIKE '%"+tag+"%'"           
            elif search and tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date WHERE NOT Moderator_ID = '' AND WHERE NOT Moderation_date = '' AND FROM programs WHERE code LIKE '%"+search+"%'"
                for tag in tags.split(" "):
                    request += " AND WHERE code LIKE '%"+tag+"%'"
            elif language:
                request = 'SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE NOT Moderator_ID = '' AND WHERE NOT Moderation_date = '' AND WHERE Language="'+language+'"'
            elif search:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE NOT Moderator_ID = '' AND WHERE NOT Moderation_date = '' AND WHERE code LIKE '%"+search+"%'"
            elif tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM programs WHERE NOT Moderator_ID = '' AND WHERE NOT Moderation_date = ''"
                for tag in tags.split(" "):
                    request += " AND WHERE code LIKE '%"+tag+"%'"           
            with connection.cursor() as cursor:
                cursor.execute(request)
                return cursor.fetchall()
    except Error as e:
        print(e)
        return {"res": "bad"}


#Админка дальше
@app.get("/adminlogin")
def adminlogin(email: str, password: str):
    try:
        with connect(
            host="localhost:3306",
            user="root",
            password="root"
        ) as connection:
            request = "SELECT ID FROM Admins WHERE E-mail='"+email+"' AND WHERE Password='"+password+"'"
            with connection.cursor() as cursor:
                cursor.execute(request)
                return cursor.fetchall()
    except Error as e:
        print(e)
        return {"res": "bad"}

@app.get("/admingetposts")
def adminGetAllPosts(postid: str, adminid: str):
    ...

@app.get("/adminmoderatepost")
def adminModeratePost(postid: str, adminid: str, moderationdate: str, adminpassword: str):
    try:
        with connect(
            host="localhost:3306",
            user="root",
            password="root"
        ) as connection:
            request = "UPDATE programs SET Moderation_Date = '"+moderationdate+"', Moderation_ID='"+adminid+"' WHERE ID='"+postid+"' AND EXISTS (SELECT * FROM Admins WHERE ID='"+adminid+"' AND Password='"+adminpassword+"')"
            with connection.cursor() as cursor:
                cursor.execute(request)
                return {"res": "good"}
    except Error as e:
        print(e)
        return {"res": "bad"}