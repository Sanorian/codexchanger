from fastapi import FastAPI
from mysql.connector import connect, Error
from fastapi.middleware.cors import CORSMiddleware

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
    ...

#Регистрация
@app.get("/registration")
def registration(mail: str, nickname: str, password: str):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            with connection.cursor() as cursor:
                getEmail = "SELECT * FROM Users WHERE Email='"+mail+"'"
                cursor.execute(getEmail)
                if len(cursor.fetchall())!=0:
                    return {"res":"bad", "reason":"mail"}
                getName = "SELECT * FROM Users WHERE UserName='"+nickname+"'"
                cursor.execute(getName)
                if len(cursor.fetchall())!=0:
                    return {"res":"bad", "reason":"nickname"}
                request = "INSERT INTO Users (UserName, Email, Password) VALUES ('"+nickname+"', '"+mail+"', '"+password+"')"
                cursor.execute(request)
                connection.commit()
                return {"res": "good", "id": id, "password": password, "username": nickname}
    except Error as e:
        print(e)
        return {"res": "bad"}
    


#Вход
@app.get("/login")
def logIn(mail: str, password: str):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            with connection.cursor() as cursor:
                getMail = "SELECT Password FROM Users WHERE Email='" + mail + "'"
                cursor.execute(getMail)
                detectedUserPassword = cursor.fetchone()
                if detectedUserPassword == None:
                    connection.commit()
                    return {"res": "bad", "reason": "mail"}
                if detectedUserPassword[0] == password:
                    connection.commit()
                    return {"res": "good", "email": mail, "password": password}
                return {"res": "bad", "reason": "password"}
    except Error as e:
        print(e)
        return {"res": "bad"}

#Получение конкретного поста
@app.get("/getpost")
def getOnePost(postid: int):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            request = "SELECT ID, Name, Language, Tags, Publication_date, Code FROM Programs WHERE ID='"+postid+"'"
            with connection.cursor() as cursor:
                cursor.execute(request)
                postData = cursor.fetchall()
                connection.commit()
                return postData
    except Error as e:
        print(e)
        return {"res": "bad"}

#Добавление постов
@app.get("/addpost")
def addPost(userID: int, name: str, code: str, language: str, tags: str, publicationdate: str):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            with connection.cursor() as cursor:
                getIDRequest = "SELECT ID FROM Programs"
                cursor.execute(getIDRequest)
                request = "INSERT INTO Programs (User_ID, Name, Code, Language, Tags, Publication_date, Moderator_ID, Moderation_Date) VALUES ("+userID+", '"+name+"', '"+code+"', '"+ language+"', '"+tags+"', '"+publicationdate+"', '', '')"
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
            if language and search and tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM Programs WHERE NOT Moderator_ID = '' AND NOT Moderation_date = '' AND Code LIKE '%"+search+"% AND Language='"+language+"'"
                for tag in tags.split(" "):
                    request += " AND WHERE Code LIKE '%"+tag+"%'"         
            elif language and search:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM Programs WHERE NOT Moderator_ID = '' AND NOT Moderation_date = '' AND Code LIKE '%"+search+"% AND Language='"+language+"'"
            elif language and tags:
                request = 'SELECT ID, Name, Language, Tags, Publication_date FROM Programs WHERE NOT Moderator_ID = '' AND NOT Moderation_date = '' AND Language="'+language+'"'
                for tag in tags.split(" "):
                    request += " AND WHERE Code LIKE '%"+tag+"%'"           
            elif search and tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM Programs WHERE NOT Moderator_ID = '' AND NOT Moderation_date = '' AND  Code LIKE '%"+search+"%'"
                for tag in tags.split(" "):
                    request += " AND WHERE Code LIKE '%"+tag+"%'"
            elif language:
                request = 'SELECT ID, Name, Language, Tags, Publication_date FROM Programs WHERE NOT Moderator_ID = '' AND NOT Moderation_date = '' AND Language="'+language+'"'
            elif search:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM Programs WHERE NOT Moderator_ID = '' AND NOT Moderation_date = '' AND Code LIKE '%"+search+"%'"
            elif tags:
                request = "SELECT ID, Name, Language, Tags, Publication_date FROM Programs WHERE NOT Moderator_ID = '' AND NOT Moderation_date = ''"
                for tag in tags.split(" "):
                    request += " AND WHERE Code LIKE '%"+tag+"%'"           
            with connection.cursor() as cursor:
                cursor.execute(request)
                postsData = cursor.fetchall()
                connection.commit()
                return postsData
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
                if len(cursor.fetchall())==1:
                    connection.commit()
                    return {"res": "good"}
                connection.commit()
                return {"res": "bad"}
    except Error as e:
        print(e)
        return {"res": "bad"}

@app.get("/admingetposts")
def adminGetAllPosts(postid: str, adminid: str):
    ...

@app.get("/adminmoderatepost")
def adminModeratePost(postid: int, adminid: int, moderationdate: str, adminpassword: str):
    try:
        with connect(
            host="localhost",
            user="lord",
            password="lord",
            database="CodeXChanger_DB"
        ) as connection:
            request = "UPDATE Programs SET Moderation_Date = '"+moderationdate+"', Moderation_ID="+adminid+" WHERE ID="+postid+" AND EXISTS (SELECT * FROM Admins WHERE ID="+adminid+" AND Password='"+adminpassword+"')"
            with connection.cursor() as cursor:
                cursor.execute(request)
                connection.commit()
                return {"res": "good"}
    except Error as e:
        print(e)
        return {"res": "bad"}