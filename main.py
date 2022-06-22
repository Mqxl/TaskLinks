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
        <button onclick="getLocation()">Try It</button>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:9000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(showPosition)
                input.value = ''
                event.preventDefault()
            }
            function getLocation() {
                  if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition);
                  } else {
                    x.innerHTML = "Geolocation is not supported by this browser.";
                  }
                }
                
            function showPosition(position) {
                ws.send(position.coords.latitude + Math.floor(Math.random() * 5) + ", " + position.coords.longitude + Math.floor(Math.random() * 5))
            }
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
        await redis.set('data', data)
        geoLoc = Nominatim(user_agent="GetLoc")
        locname = geoLoc.reverse(data)
        await websocket.send_text(f"Message text was: {locname.address}")


@app.get('/get_data')
async def data():
    geo = await redis.get('data')
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(geo)
    return locname.address