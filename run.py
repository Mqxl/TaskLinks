from main import app
import uvicorn
import sys
import os
sys.path.append(os.path.abspath(__file__))

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='127.0.0.1',
        port=9000
    )