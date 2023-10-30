import FastAPI
from getpass import getpass
from mysql.connector import connect, Error

app = FastAPI()

@app.get("/")
def posts():
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass("Пароль: "),
        ) as connection:
            request = "****"
            with connection.cursor() as cursor:
                cursor.execute(request)
                return cursor
    except Error as e:
        print(e)
