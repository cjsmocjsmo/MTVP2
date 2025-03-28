from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import mtvtables as MTVTABS
import os
from pydantic import BaseModel
import sqlite3
from typing import List
import uvicorn
import vlc

load_dotenv()

# Initialize VLC player
instance = vlc.Instance()
player = instance.media_player_new()

app = FastAPI()

app.mount("/movstatic", StaticFiles(directory="/usr/share/MTV2/thumbnails"), name="movstatic")
app.mount("/tvstatic", StaticFiles(directory="/usr/share/MTV2/tvthumbnails"), name="tvstatic")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

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

def write_pid_file():
    pid = os.getpid()
    with open(os.getenv("MTV_PID_FILE"), "w") as f:
        f.write(str(pid))

def db_file_exists():
    return os.path.exists(os.getenv("MTV_DB_PATH"))

def mov_db_content_check():
    conn = sqlite3.connect(os.getenv("MTV_DB_PATH"))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    if len(movies) == 0:
        return False
    return True

@app.on_event("startup")
def startup():
    if not db_file_exists():
        print("DB file does not exist please run 'python3 SETUP.py -i'")
        exit(1)
    if not mov_db_content_check():
        print("DB is empty. Please run 'python3 SETUP.py -i'")
        exit(1)
    write_pid_file()

def get_media_path_from_media_id(media_id):
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Path FROM movies WHERE MovId=?", (media_id,))
    path = cursor.fetchone()
    conn.close()
    return path[0]

def get_media_path_from_tv_id(tv_id):
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Path FROM tvshows WHERE TvId=?", (tv_id,))
    path = cursor.fetchone()
    conn.close()
    return path[0]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/player_set_media/{media_id}")
def set_media(media_id: str):
    print(media_id)
    media_path = get_media_path_from_media_id(media_id)
    player.set_media(vlc.Media(media_path))
    player.set_fullscreen(True)
    return {media_path}

@app.get("/player_set_tv_media/{tvmediaid}")
def set_tv_media(tvmediaid: str):
    media_path = get_media_path_from_tv_id(tvmediaid)
    player.set_media(vlc.Media(media_path))
    player.set_fullscreen(True)
    player.play()
    return {"status": "media set"}

@app.get("/player_play")
def player_play():
    player.play()
    return {"status": "playing"}

@app.get("/player_pause")
def player_pause():
    player.pause()
    return {"status": "paused"}

@app.get("/player_stop")
def player_stop():
    player.stop()
    return {"status": "stopped"}

@app.get("/player_previous")
def player_previous():
    current_time = player.get_time()
    player.set_time(current_time - 30000)
    return {"status": "previous"}

@app.get("/player_next")
def player_next():
    current_time = player.get_time()
    player.set_time(current_time + 30000)
    return {"status": "next"}

@app.get("/movsearch/{search_term}", response_model=List[Movie])
def search(search_term: str):
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Year, PosterAddr, Size, Path, Idx, MovId, Catagory, HttpThumbPath FROM movies WHERE Name LIKE ? ORDER BY Year DESC", ('%' + search_term + '%',))
    movies = cursor.fetchall()
    conn.close()
    
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")
    
    return [Movie(Name=movie[0], Year=movie[1], PosterAddr=movie[2], Size=movie[3], Path=movie[4], Idx=movie[5], MovId=movie[6], Catagory=movie[7], HttpThumbPath=movie[8]) for movie in movies]

@app.get("/tvsearch/{search_term}/{season}", response_model=List[TVShow])
def tvsearch(search_term: str, season: str):
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Name LIKE ? AND Season=? ORDER BY Season, Episode", ('%' + search_term + '%', season))
    tvshows = cursor.fetchall()
    conn.close()
    
    if not tvshows:
        raise HTTPException(status_code=404, detail="No TV shows found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

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

@app.get("/ahsoka1", response_model=List[TVShow])
def ahsoka():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Ahsoka' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Ahsoka episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/alteredcarbon1", response_model=List[TVShow])
def alteredcarbons1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='AlteredCarbon' AND Season='01' ORDER BY Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Altered Carbon Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/alteredcarbon2", response_model=List[TVShow])
def alteredcarbons2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='AlteredCarbon' AND Season='02' ORDER BY Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Altered Carbon Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/andor", response_model=List[TVShow])
def andor():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Andor' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Andor episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/cowboybebop", response_model=List[TVShow])
def cowboybebop():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='CowboyBebop' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Cowboy Bebop episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/continental", response_model=List[TVShow])
def continental():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TheContinental' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Continental episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/badbatch1", response_model=List[TVShow])
def badbatch1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='BadBatch' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Bad Batch Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/badbatch2", response_model=List[TVShow])
def badbatch2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='BadBatch' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Bad Batch Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/badbatch3", response_model=List[TVShow])
def badbatch3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='BadBatch' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Bad Batch Season 3 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery1", response_model=List[TVShow])
def discovery1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery2", response_model=List[TVShow])
def discovery2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery3", response_model=List[TVShow])
def discovery3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 3 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery4", response_model=List[TVShow])
def discovery4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='04' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 4 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/discovery5", response_model=List[TVShow])
def discovery5():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Discovery' AND Season='05' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Discovery Season 5 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/enterprise1", response_model=List[TVShow])
def enterprise1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Enterprise' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Enterprise Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/enterprise2", response_model=List[TVShow])
def enterprise2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Enterprise' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Enterprise Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/enterprise3", response_model=List[TVShow])
def enterprise3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Enterprise' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Enterprise Season 3 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/enterprise4", response_model=List[TVShow])
def enterprise4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Enterprise' AND Season='04' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Enterprise Season 4 episodes found")

    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/falconwintersoldier", response_model=List[TVShow])
def falconwintersoldier():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='FalconWinterSoldier' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Falcon Winter Soldier episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/fallout", response_model=List[TVShow])
def fallout():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Fallout' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Fallout episodes found")

    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/foundation1", response_model=List[TVShow])
def foundation1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Foundation' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Foundation episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/foundation2", response_model=List[TVShow])
def foundation2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Foundation' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Foundation episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/fubar", response_model=List[TVShow])
def fubar():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='FuuBar' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Foobar episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/forallmankind1", response_model=List[TVShow])
def forallmankind1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='ForAllMankind' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No For All Mankind episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/forallmankind2", response_model=List[TVShow])
def forallmankind2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='ForAllManKind' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No For All Mankind episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/forallmandkind3", response_model=List[TVShow])
def forallmandkind3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='ForAllManKind' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No For All Mankind episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/forallmandkind4", response_model=List[TVShow])
def forallmandkind4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='ForAllManKind' AND Season='04' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No For All Mankind episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/halo1", response_model=List[TVShow])
def halo1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Halo' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Halo episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/halo2", response_model=List[TVShow])
def halo2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Halo' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Halo episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/hawkeye", response_model=List[TVShow])
def hawkeye():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Hawkeye' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Hawkeye episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/houseofthedragon1", response_model=List[TVShow])
def houseofthedragon1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='HouseOfTheDragon' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No House of the Dragon episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/houseofthedragon2", response_model=List[TVShow])
def houseofthedragon2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='HouseOfTheDragon' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No House of the Dragon episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/iamgroot1", response_model=List[TVShow])
def iamgroot1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='IAmGroot' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No I Am Groot episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/iamgroot2", response_model=List[TVShow])
def iamgroot2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='IAmGroot' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No I Am Groot episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lastofus", response_model=List[TVShow])
def lastofus():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TheLastOfUs' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Last of Us episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/loki1", response_model=List[TVShow])
def loki1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Loki' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Loki episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/loki2", response_model=List[TVShow])
def loki2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Loki' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Loki episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lostinspace1", response_model=List[TVShow])
def lostinspace1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='LostInSpace' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lost In Space episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lostinspace2", response_model=List[TVShow])
def lostinspace2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='LostInSpace' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lost In Space episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lostinspace3", response_model=List[TVShow])
def lostinspace3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='LostInSpace' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lost In Space episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks1", response_model=List[TVShow])
def lowerdecks1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='LowerDecks' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks2", response_model=List[TVShow])
def lowerdecks2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='LowerDecks' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks3", response_model=List[TVShow])
def lowerdecks3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='LowerDecks' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks4", response_model=List[TVShow])
def lowerdecks4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='LowerDecks' AND Season='04' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/lowerdecks5", response_model=List[TVShow])
def lowerdecks5():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='LowerDecks' AND Season='05' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Lower Decks episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/mandalorian1", response_model=List[TVShow])
def mandalorian1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Mandalorian' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Mandalorian episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/mandalorian2", response_model=List[TVShow])
def mandalorian2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Mandalorian' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Mandalorian episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/mandalorian3", response_model=List[TVShow])
def mandalorian3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Mandalorian' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Mandalorian episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/monarch", response_model=List[TVShow])
def monarch():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='MonarchLegacyOfMonsters' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Monarch episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/moonknight", response_model=List[TVShow])
def moonknight():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='MoonKnight' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Moon Knight episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/TNG1", response_model=List[TVShow])
def TNG1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TNG' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 1 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/TNG2", response_model=List[TVShow])
def TNG2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TNG' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 2 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/TNG3", response_model=List[TVShow])
def TNG3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TNG' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 3 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/TNG4", response_model=List[TVShow])
def TNG4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TNG' AND Season='04' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 4 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/TNG5", response_model=List[TVShow])
def TNG5():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TNG' AND Season='05' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 5 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/TNG6", response_model=List[TVShow])
def TNG6():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TNG' AND Season='06' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 6 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/TNG7", response_model=List[TVShow])
def TNG7():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TNG' AND Season='07' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Next Generation Season 7 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/nightsky", response_model=List[TVShow])
def nightsky():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='NightSky' And Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Night Sky episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/obiwan", response_model=List[TVShow])
def obiwan():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='ObiWanKenobi' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Obi Wan episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/orville1", response_model=List[TVShow])
def orville1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Orville' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Orville episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/orville2", response_model=List[TVShow])
def orville2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Orville' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Orville episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/orville3", response_model=List[TVShow])
def orville3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Orville' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Orville episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/picard1", response_model=List[TVShow])
def picard1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Picard' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Picard episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/picard2", response_model=List[TVShow])
def picard2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Picard' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Picard episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/prehistoricplanet", response_model=List[TVShow])
def prehistoricplanet():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='PrehistoricPlanet' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Prehistoric Planet episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/prodigy1", response_model=List[TVShow])
def prodigy1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Prodigy' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Prodigy episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/prodigy2", response_model=List[TVShow])
def prodigy2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Prodigy' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Prodigy episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]


@app.get("/skeletoncrew", response_model=List[TVShow])
def skeletoncrew():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='SkeletonCrew' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Skeleton Crew episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/strangenewworlds1", response_model=List[TVShow])
def strangenewworlds1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='StrangeNewWorlds' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Strange New Worlds episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/strangenewworlds2", response_model=List[TVShow])
def strangenewworlds2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='StrangeNewWorlds' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Strange New Worlds episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/talesofthejedi", response_model=List[TVShow])
def talesofthejedi():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TalesOfTheJedi' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Tales Of The Jedi episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/raisedbywolves1", response_model=List[TVShow])
def raisedbywolves1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='RaisedByWolves' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Raised By Wolves episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/raisedbywolves2", response_model=List[TVShow])
def raisedbywolves2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='RaisedByWolves' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Raised By Wolves episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/secretinvasion", response_model=List[TVShow])
def secretinvasion():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='SecretInvasion' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Secret Invation episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/shehulk", response_model=List[TVShow])
def shehulk():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='SheHulk' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No She Hulk episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/shogun", response_model=List[TVShow])
def shogun():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Shogun' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Shogun episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/silo1", response_model=List[TVShow])
def silo1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Silo' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Silo episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/silo2", response_model=List[Movie])
def silo2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Silo' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Silo episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/theringsofpower", response_model=List[TVShow])
def theringsofpower():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='TheLordOfTheRingsTheRingsOfPower' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No The Rings of Power episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/sttv1", response_model=List[TVShow])
def sttv1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='STTV' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Star Trek episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/sttv2", response_model=List[TVShow])
def sttv2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='STTV' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Star Trek episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/sttv3", response_model=List[TVShow])
def sttv3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='STTV' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Star Trek episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/visions1", response_model=List[TVShow])
def visions1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Visions' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Visions episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/visions2", response_model=List[TVShow])
def visions2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Visions' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Visions episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager1", response_model=List[TVShow])
def voyager1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager2", response_model=List[TVShow])
def voyager2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='02' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager3", response_model=List[TVShow])
def voyager3():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='03' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager4", response_model=List[TVShow])
def voyager4():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='04' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager5", response_model=List[TVShow])
def voyager5():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='05' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager6", response_model=List[TVShow])
def voyager6():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='06' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/voyager7", response_model=List[TVShow])
def voyager7():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='Voyager' AND Season='07' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Voyager episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/wandavision", response_model=List[TVShow])
def wandavision():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='WandaVision' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Wanda Vision episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/1923", response_model=List[TVShow])
def tv1923():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='HFord1923' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No 1923 episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/wheeloftime1", response_model=List[TVShow])
def wheeloftime1():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='WheelOfTime' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Wheel of Time episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

@app.get("/wheeloftime2", response_model=List[TVShow])
def wheeloftime2():
    conn = sqlite3.connect(os.getenv('MTV_DB_PATH'))
    cursor = conn.cursor()
    cursor.execute("SELECT TvId, Size, Catagory, Name, Season, Episode, Path, Idx FROM tvshows WHERE Catagory='WheelOfTime' AND Season='01' ORDER BY Season DESC, Episode DESC")
    tvshows = cursor.fetchall()
    conn.close()

    if not tvshows:
        raise HTTPException(status_code=404, detail="No Wheel of Time episodes found")
    
    return [TVShow(TvId=tvshow[0], Size=tvshow[1], Catagory=tvshow[2], Name=tvshow[3], Season=tvshow[4], Episode=tvshow[5], Path=tvshow[6], Idx=tvshow[7]) for tvshow in tvshows]

if __name__ == "__main__":
    load_dotenv()
    host = os.getenv("MTV_RAW_ADDR")
    port = self.config["Server"]["MTV_SERVER_PORT"]
    uvicorn.run(app, host=host, port=int(port))
    write_pid_file()