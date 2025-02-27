from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from typing import List
from pydantic import BaseModel
import mtvserverutils
import uvicorn
import sqlite3

load_dotenv()

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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Action' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No action movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/arnold", response_model=List[Movie])
def arnold():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Arnold' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Arnold movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/brucelee", response_model=List[Movie])
def brucelee():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Bruce Lee' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Bruce Lee movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("brucewillis", response_model=List[Movie])
def brucewillis():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Bruce Willis' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Bruce Willis movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/buzz", response_model=List[Movie])
def buzz():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Buzz' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Buzz movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/cartoons", response_model=List[Movie])
def cartoons():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Cartoons' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No cartoons found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/charliebrown", response_model=List[Movie])
def charliebrown():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Charlie Brown' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Charlie Brown movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/comedy", response_model=List[Movie])
def comedy():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Comedy' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No comedy movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/chucknorris", response_model=List[Movie])
def chucknorris():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Chuck Norris' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Chuck Norris movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/documentary", response_model=List[Movie])
def documentary():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Documentary' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No documentary movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/drama", response_model=List[Movie])
def drama():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Drama' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No drama movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/fantasy", response_model=List[Movie])
def fantasy():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Fantasy' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No fantasy movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/ghostbusters", response_model=List[Movie])
def ghostbusters():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Ghostbusters' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Ghostbusters movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/godzilla", response_model=List[Movie])
def godzilla():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Godzilla' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Godzilla movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/harrisonford", response_model=List[Movie])
def harrisonford():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Harrison Ford' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Harrison Ford movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/harrypotter", response_model=List[Movie])
def harrypotter():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Harry Potter' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Harry Potter movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/hellboy", response_model=List[Movie])
def hellboy():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Hellboy' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Hellboy movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/indianajones", response_model=List[Movie])
def indianajones():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Indiana Jones' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Indiana Jones movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/jamesbond", response_model=List[Movie])
def jamesbond():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='James Bond' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No James Bond movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/johnwayne", response_model=List[Movie])
def johnwayne():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='John Wayne' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No John Wayne movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/johnwick", response_model=List[Movie])
def johnwick():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='John Wick' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No John Wick movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/jurassicpark", response_model=List[Movie])
def jurassicpark():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Jurassic Park' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Jurassic Park movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/kevincostner", response_model=List[Movie])
def kevincostner():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Kevin Costner' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Kevin Costner movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/kingsman", response_model=List[Movie])
def kingsman():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Kingsman' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Kingsman movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/lego", response_model=List[Movie])
def lego():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Lego' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Lego movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/meninblack", response_model=List[Movie])
def meninblack():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='MenInBlack' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No MenInBlack movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/minions", response_model=List[Movie])
def minions():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Minions' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Minions movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/misc", response_model=List[Movie])
def misc():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Misc' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Misc movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/nicolascage", response_model=List[Movie])
def nicolascage():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Nicolas Cage' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Nicolas Cage movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/oldies", response_model=List[Movie])
def oldies():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Oldies' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Oldies movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/panda", response_model=List[Movie])
def panda():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Panda' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Panda movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/pirates", response_model=List[Movie])
def pirates():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Pirates' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Pirates movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/riddick", response_model=List[Movie])
def riddick():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Riddick' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Riddick movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/scifi", response_model=List[Movie])
def scifi():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='SciFi' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No SciFi movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/stalone", response_model=List[Movie])
def stalone():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Stalone' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Stalone movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/startrek", response_model=List[Movie])
def startrek():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Star Trek' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Star Trek movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/starwars", response_model=List[Movie])
def starwars():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Star Wars' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Star Wars movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/superheros", response_model=List[Movie])
def superheros():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Superheros' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Superheros movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/therock", response_model=List[Movie])
def therock():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='The Rock' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No The Rock movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/tinkerbell", response_model=List[Movie])
def tinkerbell():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Tinkerbell' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Tinkerbell movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/tomcruise", response_model=List[Movie])
def tomcruise():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Tom Cruise' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Tom Cruise movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/transformers", response_model=List[Movie])
def transformers():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Transformers' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Transformers movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/tremors", response_model=List[Movie])
def tremors():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Tremors' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Tremors movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/vandam", response_model=List[Movie])
def vandam():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='Van Dam' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Van Dam movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/xmen", response_model=List[Movie])
def xmen():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='XMen' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No XMen movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]




@app.get("/alteredcarbons1", response_model=List[Movie])
def alteredcarbons1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Season='1' ORDER BY Episode DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Altered Carbon Season 1 episodes found")
    
    return [Movie(TvId=movie[0], Size=movie[1], Catagory=movie[2], Name=movie[3], Season=movie[4], Episode=movie[5], Path=movie[6], Idx=movie[7]) for movie in movies]

@app.get("/alteredcarbons2", response_model=List[Movie])
def alteredcarbons2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Season='2' ORDER BY Episode DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Altered Carbon Season 2 episodes found")
    
    return [Movie(TvId=movie[0], Size=movie[1], Catagory=movie[2], Name=movie[3], Season=movie[4], Episode=movie[5], Path=movie[6], Idx=movie[7]) for movie in movies]


    


if __name__ == "__main__":
    host = os.getenv("MTV_RAW_ADDR")
    port = int(os.getenv("MTV_SERVER_PORT"))
    
    uvicorn.run(app, host=host, port=port)