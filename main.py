import asyncio
import time
from typing import List

from fastapi import FastAPI, Depends, WebSocket
from starlette.websockets import WebSocketDisconnect

from alembic.devsettings import redis
from geopy.geocoders import Nominatim
from argon2 import PasswordHasher
from argon2 import exceptions
from auth import AuthHandler
from payloads.loginpayload import AuthDetails
from provider.basestmt import user_get_stmt

app = FastAPI()
ph = PasswordHasher()
auth_handler = AuthHandler()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>SendData</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <button onclick="newfunc()">Try It</button>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:9000/ws/1");
            const getRandom = () => {
              let random = Math.random() * 150;
              let random2 = Math.random() * 150;
              let dictionary = {
                longitude: random,
                latitude: random2
              }
              console.log(dictionary)
              ws.send(JSON.stringify(dictionary))
            }
            const newfunc = () => {
            console.log('111')
                setInterval(()=>{
                  getRandom()
                },500)
            }
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""
manager = ConnectionManager()

@app.get("/")
async def get():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(html)


@app.post('/login/')
async def login(
    auth_details: AuthDetails
):
    users = await user_get_stmt(auth_details.username)
    try:
        ph.verify(users.password, password=auth_details.password)
        token = auth_handler.encode_token(users.name)
        return {'token': token}
    except exceptions.VerifyMismatchError:
        return {"message": "Enter correct password or username"}


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await redis.set('data', data)
#         await websocket.send_text(f"Message text was: {data}")

@app.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await redis.set('data', data)
            await manager.broadcast(f"{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user} left the chat")