from fastapi import FastAPI, Depends, WebSocket
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

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <button onclick="newfunc()">Try It</button>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:9000/ws");
            const getRandom = () => {
              let random = Math.random() * 150;
              let random2 = Math.random() * 150;
              let dictionary = {
                long: random,
                latt: random2
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        await redis.set('data', data)
        await websocket.send_text(f"Message text was: {data}")


@app.get('/get_data')
async def data():
    geo = await redis.get('data')
    return geo