from fastapi import FastAPI
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
