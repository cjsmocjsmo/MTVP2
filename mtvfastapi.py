from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
from typing import List
from pydantic import BaseModel
# import mtvserverutils
import uvicorn
import sqlite3

load_dotenv()

# MTVMEDIA = mtvserverutils.Media()

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.mount("/static", StaticFiles(directory="/home/pimedia/MTV2/MTVP2/frontend"), name="static")

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

class TVShow(BaseModel):
    TvId: str
    Size: str
    Catagory: str
    Name: str
    Season: str
    Episode: str
    Path: str
    Idx: str

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return FileResponse("./frontend/index.html")

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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='BruceLee' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Bruce Lee movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/brucewillis", response_model=List[Movie])
def brucewillis():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='BruceWillis' ORDER BY Year DESC")
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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='CharlieBrown' ORDER BY Year DESC")
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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='ChuckNorris' ORDER BY Year DESC")
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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='GhostBusters' ORDER BY Year DESC")
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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='HarrisonFord' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Harrison Ford movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/harrypotter", response_model=List[Movie])
def harrypotter():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='HarryPotter' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Harry Potter movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/hellboy", response_model=List[Movie])
def hellboy():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='HellBoy' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Hellboy movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/indianajones", response_model=List[Movie])
def indianajones():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='IndianaJones' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Indiana Jones movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/jamesbond", response_model=List[Movie])
def jamesbond():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='JamesBond' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No James Bond movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/johnwayne", response_model=List[Movie])
def johnwayne():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='JohnWayne' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No John Wayne movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/johnwick", response_model=List[Movie])
def johnwick():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='JohnWick' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No John Wick movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/jurrasicpark", response_model=List[Movie])
def jurrasicpark():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='JurrasicPark' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No Jurassic Park movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/kevincostner", response_model=List[Movie])
def kevincostner():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='KevinCostner' ORDER BY Year DESC")
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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='NicolasCage' ORDER BY Year DESC")
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

@app.get("/pandas", response_model=List[Movie])
def pandas():
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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='StarTrek' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Star Trek movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/starwars", response_model=List[Movie])
def starwars():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='StarWars' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Star Wars movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/superheros", response_model=List[Movie])
def superheros():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='SuperHeros' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Superheros movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/therock", response_model=List[Movie])
def therock():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='TheRock' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No The Rock movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/tinkerbell", response_model=List[Movie])
def tinkerbell():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='TinkerBell' ORDER BY Year DESC")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        raise HTTPException(status_code=404, detail="No Tinkerbell movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/tomcruise", response_model=List[Movie])
def tomcruise():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='TomCruize' ORDER BY Year DESC")
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
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Catagory='VanDam' ORDER BY Year DESC")
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

########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################

@app.get("/ahsoka", response_model=List[TVShow])
def ahsoka():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Ahsoka' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Ahsoka episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/alteredcarbon1", response_model=List[TVShow])
def alteredcarbons1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Season='1' ORDER BY Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Altered Carbon Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/alteredcarbon2", response_model=List[TVShow])
def alteredcarbons2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Season='2' ORDER BY Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Altered Carbon Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/andor", response_model=List[TVShow])
def andor():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Andor' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Andor episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/cowboybebop", response_model=List[TVShow])
def cowboybebop():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Cowboy Bebop' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Cowboy Bebop episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/continental", response_model=List[TVShow])
def continental():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Continental' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Continental episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/badbatch1", response_model=List[TVShow])
def badbatch1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Bad Batch' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Bad Batch Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/badbatch2", response_model=List[TVShow])
def badbatch2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Bad Batch' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Bad Batch Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/badbatch3", response_model=List[TVShow])
def badbatch3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Bad Batch' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Bad Batch Season 3 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery1", response_model=List[TVShow])
def discovery1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery2", response_model=List[TVShow])
def discovery2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery3", response_model=List[TVShow])
def discovery3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 3 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery4", response_model=List[TVShow])
def discovery4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='4' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 4 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery5", response_model=List[TVShow])
def discovery5():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='5' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 5 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/enterprise1", response_model=List[TVShow])
def enterprise1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Enterprise' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Enterprise Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/enterprise2", response_model=List[TVShow])
def enterprise2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Enterprise' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Enterprise Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/enterprise3", response_model=List[TVShow])
def enterprise3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Enterprise' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Enterprise Season 3 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/enterprise4", response_model=List[TVShow])
def enterprise4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Enterprise' AND Season='4' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Enterprise Season 4 episodes found")

    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/falconwintersoldier", response_model=List[TVShow])
def falconwintersoldier():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Falcon Winter Soldier' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Falcon Winter Soldier episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/fallout", response_model=List[TVShow])
def fallout():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Fallout' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Fallout episodes found")

    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/foundation1", response_model=List[TVShow])
def foundation1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Foundation' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Foundation episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/foundation2", response_model=List[TVShow])
def foundation2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Foundation' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Foundation episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/foobar", response_model=List[TVShow])
def foobar():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Foobar' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Foobar episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/forallmankind1", response_model=List[TVShow])
def forallmankind1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='For All Mankind' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No For All Mankind episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/forallmankind2", response_model=List[TVShow])
def forallmankind2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='For All Mankind' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No For All Mankind episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/forallmandkind3", response_model=List[TVShow])
def forallmandkind3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='For All Mankind' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No For All Mankind episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/forallmandkind4", response_model=List[TVShow])
def forallmandkind4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='For All Mankind' AND Season='4' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No For All Mankind episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/halo1", response_model=List[TVShow])
def halo1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Halo' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Halo episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/halo2", response_model=List[TVShow])
def halo2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Halo' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Halo episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/hawkeye", response_model=List[TVShow])
def hawkeye():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Hawkeye' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Hawkeye episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/houseofthedragon1", response_model=List[TVShow])
def houseofthedragon1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='House Of The Dragon' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No House of the Dragon episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/houseofthedragon2", response_model=List[TVShow])
def houseofthedragon2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='House Of The Dragon' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No House of the Dragon episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/iamgroot1", response_model=List[TVShow])
def iamgroot1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='I Am Groot' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No I Am Groot episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/iamgroot2", response_model=List[TVShow])
def iamgroot2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='I Am Groot' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No I Am Groot episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lastofus", response_model=List[TVShow])
def lastofus():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Last Of Us' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Last of Us episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/loki1", response_model=List[TVShow])
def loki1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Loki' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Loki episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/loki2", response_model=List[TVShow])
def loki2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Loki' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Loki episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lostinspace1", response_model=List[TVShow])
def lostinspace1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Lost In Space' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lost In Space episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lostinspace2", response_model=List[TVShow])
def lostinspace2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Lost In Space' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lost In Space episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lostinspace3", response_model=List[TVShow])
def lostinspace3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Lost In Space' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lost In Space episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks1", response_model=List[TVShow])
def lowerdecks1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Lower Decks' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks2", response_model=List[TVShow])
def lowerdecks2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Lower Decks' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks3", response_model=List[TVShow])
def lowerdecks3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Lower Decks' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks4", response_model=List[TVShow])
def lowerdecks4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Lower Decks' AND Season='4' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks5", response_model=List[TVShow])
def lowerdecks5():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Lower Decks' AND Season='5' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/mandalorian1", response_model=List[TVShow])
def mandalorian1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Mandalorian' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Mandalorian episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/mandalorian2", response_model=List[TVShow])
def mandalorian2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Mandalorian' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Mandalorian episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/mandalorian3", response_model=List[TVShow])
def mandalorian3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Mandalorian' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Mandalorian episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/monarch", response_model=List[TVShow])
def monarch():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Monarch' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Monarch episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/moonknight", response_model=List[TVShow])
def moonknight():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Moon Knight' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Moon Knight episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nextgeneration1", response_model=List[TVShow])
def nextgeneration1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Next Generation' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nextgeneration2", response_model=List[TVShow])
def nextgeneration2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Next Generation' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nextgeneration3", response_model=List[TVShow])
def nextgeneration3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Next Generation' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 3 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nextgeneration4", response_model=List[TVShow])
def nextgeneration4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Next Generation' AND Season='4' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 4 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nextgeneration5", response_model=List[TVShow])
def nextgeneration5():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Next Generation' AND Season='5' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 5 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nextgeneration6", response_model=List[TVShow])
def nextgeneration6():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Next Generation' AND Season='6' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 6 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nextgeneration7", response_model=List[TVShow])
def nextgeneration7():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Next Generation' AND Season='7' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 7 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nightsky", response_model=List[TVShow])
def nightsky():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Night Sky' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Night Sky episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/obiwan", response_model=List[TVShow])
def obiwan():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Obi Wan' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Obi Wan episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/oreville1", response_model=List[TVShow])
def oreville1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Orville' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Orville episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/oreville2", response_model=List[TVShow])
def oreville2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Orville' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Orville episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/oreville3", response_model=List[TVShow])
def oreville3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Orville' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Orville episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/picard1", response_model=List[TVShow])
def picard1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Picard' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Picard episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/picard2", response_model=List[TVShow])
def picard2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Picard' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Picard episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/prehistoricplanet", response_model=List[TVShow])
def prehistoricplanet():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Prehistoric Planet' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Prehistoric Planet episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/prodigy", response_model=List[TVShow])
def prodigy():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Prodigy' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Prodigy episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/skeletoncrew", response_model=List[TVShow])
def skeletoncrew():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Skeleton Crew' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Skeleton Crew episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/strangenewworlds1", response_model=List[TVShow])
def strangenewworlds1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Strange New Worlds' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Strange New Worlds episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/strangenewworlds2", response_model=List[TVShow])
def strangenewworlds2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Strange New Worlds' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Strange New Worlds episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/talesofthejedi", response_model=List[TVShow])
def talesofthejedi():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Tales Of The Jedi' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Tales Of The Jedi episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/raisedbywolves1", response_model=List[TVShow])
def raisedbywolves1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Raised By Wolves' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Raised By Wolves episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/raisedbywolves2", response_model=List[TVShow])
def raisedbywolves2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Raised By Wolves' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Raised By Wolves episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/secretinvation", response_model=List[TVShow])
def secretinvation():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Secret Invation' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Secret Invation episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/shehulk", response_model=List[TVShow])
def shehulk():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='She Hulk' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No She Hulk episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/shogun", response_model=List[TVShow])
def shogun():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Shogun' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Shogun episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/silo1", response_model=List[TVShow])
def silo1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Silo' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Silo episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/silo2", response_model=List[Movie])
def silo2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Silo' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Silo episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/theringsofpower", response_model=List[TVShow])
def theringsofpower():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='The Rings of Power' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No The Rings of Power episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/sttv1", response_model=List[TVShow])
def sttv1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Star Trek' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Star Trek episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/sttv2", response_model=List[TVShow])
def sttv2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Star Trek' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Star Trek episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/sttv3", response_model=List[TVShow])
def sttv3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Star Trek' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Star Trek episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/visions1", response_model=List[TVShow])
def visions1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Visions' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Visions episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/visions2", response_model=List[TVShow])
def visions2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Visions' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Visions episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager1", response_model=List[TVShow])
def voyager1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='1' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager2", response_model=List[TVShow])
def voyager2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='2' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager3", response_model=List[TVShow])
def voyager3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='3' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager4", response_model=List[TVShow])
def voyager4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='4' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager5", response_model=List[TVShow])
def voyager5():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='5' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager6", response_model=List[TVShow])
def voyager6():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='6' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager7", response_model=List[TVShow])
def voyager7():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='7' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/wandavision", response_model=List[TVShow])
def wandavision():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Wanda Vision' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Wanda Vision episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/1923", response_model=List[TVShow])
def w1923():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='1923' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No 1923 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/wheeloftime1", response_model=List[TVShow])
def wheeloftime1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Wheel of Time' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Wheel of Time episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/wheeloftime2", response_model=List[TVShow])
def wheeloftime2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Wheel of Time' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Wheel of Time episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

if __name__ == "__main__":
    load_dotenv()
    host = os.getenv("MTV_RAW_ADDR")
    port = os.getenv("MTV_SERVER_PORT")
    uvicorn.run(app, host=host, port=int(port))