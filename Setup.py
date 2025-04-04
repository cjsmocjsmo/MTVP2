#!/usr/bin/env python3

from mtvfastapi import app
import update
import argparse
import main
import os
import utils
import uvicorn
import yaml
import sqlite3
import shutil
import subprocess

with open('./config.yaml', 'r') as f:
    config = yaml.safe_load(f)

IS_SETUP = False
if os.path.exists(config['DBs']['MTV_DB_PATH']):
    print("DB exists")
    conn = sqlite3.connect(config['DBs']['MTV_DB_PATH'])
    cursor = conn.cursor()
    movs = cursor.execute("SELECT * FROM movies").fetchall()
    tvshows = cursor.execute("SELECT * FROM tvshows").fetchall()
    conn.close()
    if len(movs) > 0 and len(tvshows) > 0:
        IS_SETUP = True
    elif len(movs) == 0 and len(tvshows) == 0:
        IS_SETUP = False
    elif len(movs) > 0 and len(tvshows) == 0:
        exit("Movs are setup TVShows are not. Clean the DB")
    elif len(movs) == 0 and len(tvshows) > 0:
        exit("TVShows are setup Movs are not. Clean the DB")
    else:
        print("WTF")

if not utils.sqlite3_check():
    print("Sqlite3 is not installed. Install with:\n")
    print("\t'sudo apt-get -y install sqlite3'")
    exit()
if not utils.vlc_check():
    print("VLC is not installed. Install with:\n")
    print("\tsudo apt-get -y install vlc")
    exit()
if not utils.python3_vlc_check():
    print("Python3 VLC is not installed. Install with:\n")
    print("\tsudo apt-get -y install python3-vlc")
    exit()
if not utils.python3_pil_check():
    print("Python3 PIL is not installed. Install with:\n")
    print("\tsudo apt-get -y install python3-pil")
    exit()
if not utils.python3_dotenv_check():
    print("Python3 dotenv is not installed. Install with:\n")
    print("\tsudo apt-get -y install python3-dotenv")
    exit()
if not utils.python3_websockets_check():
    print("Python3 websockets is not installed. Install with:\n")
    print("\tsudo apt-get -y install python3-websockets")
    exit()

def setup():
    parser = argparse.ArgumentParser(description="CLI for Rusic music server.")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete the program")
    parser.add_argument("-i", "--install", action="store_true", help="Install the program")
    parser.add_argument("-r", "--restart", action="store_true", help="Restart the program")
    parser.add_argument("-u", "--update", action="store_true", help="Update the program")
    

    args = parser.parse_args()
    
    if args.install:
        if not os.path.exists(config['Thumbnails']['MTV_THUMBNAIL_PATH']):
            os.makedirs(config['Thumbnails']['MTV_THUMBNAIL_PATH'])
            print("Thumbnails dir created")
        if not os.path.exists(config['Thumbnails']['MTV_TVTHUMBNAIL_PATH']):
            os.makedirs(config['Thumbnails']['MTV_TVTHUMBNAIL_PATH'])
            print("TV Thumbnails dir created")

        main.Main(config).main()

        # if not os.path.exists('/etc/systemd/system/mtvfastapi.service'):
        #     print("no service file found move it over dumbass")
        #     exit(1)

        # subprocess.run(['systemctl', 'daemon-reload'])
        # subprocess.run(['systemctl', 'enable', 'mtvfastapi'])
        # subprocess.run(['systemctl', 'start', 'mtvfastapi'])
        uvicorn.run(app, host=config['Server']['MTV_RAW_ADDR'], port=config['Server']['MTV_SERVER_PORT'], log_level="info", workers=1)
        print("Service started")
        
    elif args.restart:
        subprocess.run(['systemctl', 'restart', 'mtvfastapi'])
        print("Service restarted")

    elif args.update:
        subprocess.run(['systemctl', 'stop', 'mtvfastapi'])
        update.UpdateMain(config).main()
        subprocess.run(['systemctl', 'daemon-reload'])
        subprocess.run(['systemctl', 'start', 'mtvfastapi'])
        print("Service updated and started")

    elif args.delete:
        subprocess.run(['systemctl', 'stop', 'mtvfastapi'])
        subprocess.run(['systemctl', 'disable', 'mtvfastapi'])
        subprocess.run(['systemctl', 'daemon-reload'])
        os.remove('/etc/systemd/system/mtvfastapi.service')
        os.remove(config['DBs']['MTV_DB_PATH'])
        shutil.rmtree(config['Thumbnails']['MTV_THUMBNAIL_PATH'])
        shutil.rmtree(config['Thumbnails']['MTV_TVTHUMBNAIL_PATH'])
        shutil.rmtree(config['Paths']['MTV_PROG_PATH'])
        print("Service stopped and removed")

if __name__ == "__main__":
    setup()