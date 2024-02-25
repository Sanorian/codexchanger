from fastapi import FastAPI
from mysql.connector import connect, Error
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Получение всех постов, но без Moderator_id, Moderation_time и Code
@app.get("/")
def getDataAll():
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            with connection.cursor() as cursor:
                query = "SELECT ID, User_ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs ORDER BY ID DESC"
                cursor.execute(query)
                posts = cursor.fetchall()
                return {"res": "good", "posts": posts}
    except Error as e:
        print(e)
        return {"res": "bad"}

class RegistrationModel(BaseModel):
    mail: str
    nickname: str
    password: str

#Регистрация
@app.post("/registration")
def registration(model: RegistrationModel):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            with connection.cursor() as cursor:
                getEmail = f"SELECT * FROM Users WHERE Email='{model.mail}'"
                cursor.execute(getEmail)
                if len(cursor.fetchall())!=0:
                    return {"res":"bad", "reason":"mail"}
                getName = f"SELECT * FROM Users WHERE UserName='{model.nickname}'"
                cursor.execute(getName)
                if len(cursor.fetchall())!=0:
                    return {"res":"bad", "reason":"nickname"}
                request = f"INSERT INTO Users (UserName, Email, Password) VALUES ('{model.nickname}', '{model.mail}', '{model.password}')"
                cursor.execute(request)
                connection.commit()
                return {"res": "good", "password": model.password, "username": model.nickname}
    except Error as e:
        print(e)
        return {"res": "bad"}
    

class LoginModel(BaseModel):
    mail: str
    password: str

#Вход
@app.post("/login")
def logIn(model: LoginModel):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            with connection.cursor() as cursor:
                getMail = f"SELECT Password, UserName FROM Users WHERE Email='{model.mail}'"
                cursor.execute(getMail)
                detectedUserPassword = cursor.fetchone()
                if detectedUserPassword == None:
                    return {"res": "bad", "reason": "mail"}
                if detectedUserPassword[0] == model.password:
                    return {"res": "good", "username": detectedUserPassword[1], "password": model.password}
                return {"res": "bad", "reason": "password"}
    except Error as e:
        print(e)
        return {"res": "bad"}

class GetPostModel(BaseModel):
    postid: str

#Получение конкретного поста
@app.post("/getpost")
def getOnePost(model: GetPostModel):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            request = f"SELECT ProgramName, CodeLanguage, Tags, Code FROM Programs WHERE ID={model.postid}"
            with connection.cursor() as cursor:
                cursor.execute(request)
                postData = cursor.fetchone()
                if postData == None:
                    return {"res": "bad", "reason": "postid"}
                return {"res":"good", "post": postData}
    except Error as e:
        print(e)
        return {"res": "bad"}

#Добавление постов
class AddPostModel(BaseModel):
    username: str
    name: str
    code: str
    tags: str
    language: str
    publicationdate: str

@app.put("/addpost")
def addPost(model: AddPostModel):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            with connection.cursor() as cursor:
                request = f"INSERT INTO Programs (User_ID, ProgramName, Code, CodeLanguage, Tags, PublicationDate) VALUES ((SELECT ID FROM Users WHERE Username='{model.username}), '{model.name}', '{model.code}', '{model.language}', '{model.tags}', '{model.publicationdate}')"
                cursor.execute(request)
                connection.commit()
                return {"res": "good"}
    except Error as e:
        print(e)
        return {"res": "bad"}

#Получение постов с условием
@app.get("/getposts")
def getPosts(search: str | None = None, language: str | None = None, tags: str | None = None):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            request = "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs"
            if language and search and tags:
                request = "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE Code LIKE '%"+search+"%' AND CodeLanguage='"+language+"' INTERSECT "
                for tag in tags.split(" "):
                    request += "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE Tags LIKE '%"+tag+"%' INTERSECT "
                request = request.rsplit(' INTERSECT ', 1)[0]
            elif language and search:
                request = "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE Code LIKE '%"+search+"%' AND CodeLanguage='"+language+"'"
            elif language and tags:
                request = "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE CodeLanguage='"+language+"' INTERSECT "
                for tag in tags.split(" "):
                    request += "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE Tags LIKE '%"+tag+"%' INTERSECT "
                request = request.rsplit(' INTERSECT ', 1)[0]
            elif search and tags:
                request = "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE Code LIKE '%"+search+"%' INTERSECT "
                for tag in tags.split(" "):
                    request += "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE Tags LIKE '%"+tag+"%' INTERSECT "
                request = request.rsplit(' INTERSECT ', 1)[0]
            elif language:
                request = "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE CodeLanguage='"+language+"'"
            elif search:
                request = "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE Code LIKE '%"+search+"%'"
            elif tags:
                request = ""
                for tag in tags.split(" "):
                    request += "SELECT ID, ProgramName, CodeLanguage, Tags, PublicationDate FROM Programs WHERE Tags LIKE '%"+tag+"%' INTERSECT "
                request = request.rsplit(' INTERSECT ', 1)[0]
            request += " ORDER BY ID DESC"
            with connection.cursor() as cursor:
                cursor.execute(request)
                postsData = cursor.fetchall()
                return {"res":"good", "posts": postsData}
    except Error as e:
        print(e)
        return {"res": "bad"}


#Админка дальше
@app.get("/adminlogin")
def adminlogin(email: str, password: str):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            request = "SELECT ID FROM Admins WHERE Email='"+email+"' AND Password='"+password+"'"
            with connection.cursor() as cursor:
                cursor.execute(request)
                adminAccount = cursor.fetchone()
                if adminAccount == None:
                    return {"res": "bad"}
                return {"res": "good"}
    except Error as e:
        print(e)
        return {"res": "bad"}

@app.get("/admingetposts")
def adminGetAllPosts(password: str, adminid: str):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            request = "SELECT * FROM Programs WHERE Moderator_ID = NULL AND ModerationDate = NULL AND EXISTS(SELECT * FROM Admins WHERE ID="+adminid+" AND Password='"+password+"')"
            with connection.cursor() as cursor:
                cursor.execute(request)
                postsData = cursor.fetchall()
                return {"res":"good", "posts": postsData}
    except Error as e:
        print(e)
        return {"res": "bad"}

@app.get("/adminmoderatepost")
def adminModeratePost(postid: str, adminid: str, moderationdate: str, adminpassword: str):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            request = "UPDATE Programs SET ModerationDate = '"+moderationdate+"', Moderator_ID="+adminid+" WHERE ID="+postid+" AND EXISTS (SELECT * FROM Admins WHERE ID="+adminid+" AND Password='"+adminpassword+"')"
            with connection.cursor() as cursor:
                cursor.execute(request)
                connection.commit()
                return {"res": "good"}
    except Error as e:
        print(e)
        return {"res": "bad"}
