from fastapi import FastAPI
from dotenv import load_dotenv
import os
import mtvserverutils
import uvicorn

MTVMEDIA = mtvserverutils.Media()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastApi Hello, World!"}

@app.get("/action")
def action():
    return {MTVMEDIA.action()}

if __name__ == "__main__":
    
    load_dotenv()

    host = os.getenv("MTV_RAW_ADDR")
    port = os.getenv("MTV_SERVER_PORT")
    
    uvicorn.run(app, host=host, port=port)