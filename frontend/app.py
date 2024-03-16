from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import aiofiles
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

index = None
create_post = None
login = None
registration = None
post = None

@app.on_event("startup")
async def startup_event():
    global index, create_post, login, registration, post
    async with aiofiles.open('pages/index.html', mode='r') as f:
        index = await f.read()
    async with aiofiles.open('pages/create_post.html', mode='r') as f:
        create_post = await f.read()
    async with aiofiles.open('pages/login.html', mode='r') as f:
        login = await f.read()
    async with aiofiles.open('pages/registration.html', mode='r') as f:
        registration = await f.read()
    async with aiofiles.open('pages/read_post.html', mode='r') as f:
        post = await f.read()

@app.get('/', response_class=HTMLResponse)
async def index():
    global index
    return index

@app.get('/post', response_class=HTMLResponse)
async def post():
    global post
    return post

@app.get('/create_post', response_class=HTMLResponse)
async def post():
    global create_post
    return create_post

@app.get('/login', response_class=HTMLResponse)
async def post():
    global login
    return login

@app.get('/registration', response_class=HTMLResponse)
async def post():
    global registration
    return registration

@app.get('/create_post', response_class=HTMLResponse)
async def post():
    global registration
    return registration