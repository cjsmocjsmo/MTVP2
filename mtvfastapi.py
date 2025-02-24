from fastapi import FastAPI
from dotenv import load_dotenv
import os
from typing import List
from pydantic import BaseModel
import mtvserverutils
import uvicorn
import sqlite3

MTVMEDIA = mtvserverutils.Media()

app = FastAPI()

def init_db():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name str,
            Year str,
            PosterAddr str,
            Size str,
            Path str,
            Idx str,
            MovId str UNIQUE,
            Catagory str,
            HttpThumbPath str
        )""")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tvshows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TvId str UNIQUE,
            Size str,
            Catagory str,
            Name str,
            Season str,
            Episode str,
            Path str,
            Idx str
         )""")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ImgId str,
            Path str,
            ImgPath str,
            Size str,
            Name str,
            ThumbPath str,
            Idx INTEGER NOT NULL,
            HttpThumbPath str
         )""")
    conn.commit()
    conn.close()

class Movie(BaseModel):
    Name: str
    Year: str
    PosterAddr: str
    Size: str
    Path: str
    Idx: str
    MovId: str
    Catagory: str
    HttpThumbPath: str

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "FastApi Hello, World!"}

@app.get("/action", response_model=List[Movie])
def action():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE catagory='Action' ORDER BY year DESC")
    data = cursor.fetchall()
    print(data)
    conn.close()
    return [{"Name": data.Name, "Year": data.Year, "PosterAddr": data.PosterAddr, "Size": data.Size, "Path": data.Path, "Idx": data.Idx, "MovId": data.MovId, "Catagory": data.Catagory, "HttpThumbPath": data.HttpThumbPath} for data in data]

    

if __name__ == "__main__":
    
    load_dotenv()

    host = os.getenv("MTV_RAW_ADDR")
    port = os.getenv("MTV_SERVER_PORT")
    
    uvicorn.run(app, host=host, port=port)