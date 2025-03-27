#!/usr/bin/env python3
import argparse
import main
import os
import subprocess
from pprint import pprint
from dotenv import load_dotenv
import utils
import uvicorn
from mtvfastapi import app

CWD = os.getcwd()

def setup():
    parser = argparse.ArgumentParser(description="CLI for Rusic music server.")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete the program")
    parser.add_argument("-i", "--install", action="store_true", help="Install the program")
    parser.add_argument("-r", "--restart", action="store_true", help="Restart the program")
    parser.add_argument("-u", "--update", action="store_true", help="Update the program")
    

    args = parser.parse_args()
    
    if args.install:
        print(f"utils.sqlite3_check(): {utils.sqlite3_check()}")
        print(f"utils.vlc_check(): {utils.vlc_check()}")
        print(f"utils.python3_vlc_check(): {utils.python3_vlc_check()}")
        print(f"utils.python3_pil_check(): {utils.python3_pil_check()}")
        print(f"utils.python3_dotenv_check(): {utils.python3_dotenv_check()}")
        print(f"utils.python3_websockets_check(): {utils.python3_websockets_check()}")

        if not utils.sqlite3_check():
            print("Sqlite3 is not installed. Install with:\n")
            print("\tsudo apt-get -y install sqlite3")
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

        main.Main().main()
        
        if utils.get_arch() == "32":
            subprocess.run([
                "docker", 
                "build", 
                "-t", 
                "thumbnails32:latest", 
                "-f", 
                "./arch32/thumbnails/Dockerfile", 
                ".",
            ])
            subprocess.run(["docker", "run", "-d", "-p", "9090:80", "thumbnails32:latest"])
     
            subprocess.run([
                "docker", 
                "build", 
                "-t", 
                "tvthumbnails32:latest", 
                "-f", 
                "./arch32/tvthumbnails/Dockerfile", 
                ".",
            ])
            subprocess.run(["docker", "run", "-d", "-p", "9095:80", "tvthumbnails32:latest"])
        elif utils.get_arch() == "64":
            subprocess.run([
                "docker", 
                "run", 
                "-d",
                "-v",
                "/usr/share/MTV2/thumbnails:/usr/share/nginx/html/",
                "-p", 
                "9090:80",
                "--name",
                "thumbnails64",
                "nginx:bookworm",
            ])
            subprocess.run([
                "docker", 
                "run", 
                "-d",
                "-v",
                "/usr/share/MTV2/tvthumbnails:/usr/share/nginx/html/",
                "-p", 
                "9095:80",
                "--name",
                "tvthumbnails64",
                "nginx:bookworm",
            ])
        host = os.getenv("MTV_RAW_ADDR")
        port = os.getenv("MTV_SERVER_PORT")
        uvicorn.run(app, host=host, port=int(port))
        
    elif args.restart:
        pid_path = os.getenv("MTV_PID_PATH")
        with open(pid_path, "r") as f:
            pid = f.read()
        if pid:
            subprocess.run(["kill", pid])

        db_path = os.getenv("MTV_DB_PATH")
        if not os.path.exists(db_path):
            print(f"Database file not found at {db_path}. Please ensure the database is present.\nYou may want to run 'python3 SETUP.py -i'")
            exit()

        containers = subprocess.run(("docker", "ps", "-aq"))
        if len(containers) == 0:
            print("No containers found. Please run 'python3 SETUP.py -i'.")
            exit()
        else:
            for container in containers:
                subprocess.run(("docker", "start", container))
        
        main.Main().main()
        host = os.getenv("MTV_RAW_ADDR")
        port = os.getenv("MTV_SERVER_PORT")
        uvicorn.run(app, host=host, port=int(port))

    elif args.update:
        pid_path = os.getenv("MTV_PID_PATH")
        with open(pid_path, "r") as f:
            pid = f.read()
        if pid:
            subprocess.run(["kill", pid])

        containers = subprocess.run(("docker", "ps", "-aq"))
        if len(containers) != 0:
            for container in containers:
                subprocess.run(("docker", "stop", container))
                subprocess.run(("docker", "rm", container))

        subprocess.run(("sudo", "rm", "-rf", os.getenv("MTV_DB_PATH")))
        subprocess.run(("sudo", "rm", "-rf", os.getenv("MTV_THUMBNAIL_PATH")))
        subprocess.run(("sudo", "rm", "-rf", os.getenv("MTV_TVTHUMBNAIL_PATH")))
        subprocess.run(("sudo", "rm", "-rf", os.getenv("MTV_PID_FILE")))

        main.Main().main()
        if utils.get_arch() == "32":
            subprocess.run([
                "docker", 
                "run", 
                "-d", 
                "-v",
                "/usr/share/MTV2/thumbnails:/usr/share/nginx/html/",
                "--name",
                "thumbnails32",
                "-p", 
                "9090:80", 
                "arm32v7/nginx:bookworm",
            ])
            subprocess.run([
                "docker", 
                "run", 
                "-d",
                "-v",
                "/usr/share/MTV2/tvthumbnails:/usr/share/nginx/html/",
                "--name",
                "tvthumbnails32",
                "-p", 
                "9095:80", 
                "arm32v7/nginx:bookworm",
            ])
        elif utils.get_arch() == "64":
            subprocess.run([
                "docker", 
                "run", 
                "-d",
                "-v",
                "/usr/share/MTV2/thumbnails:/usr/share/nginx/html/",
                "-p", 
                "9090:80",
                "--name",
                "thumbnails64",
                "nginx:bookworm",
            ])
            subprocess.run([
                "docker", 
                "run", 
                "-d",
                "-v",
                "/usr/share/MTV2/tvthumbnails:/usr/share/nginx/html/",
                "-p", 
                "9095:80",
                "--name",
                "tvthumbnails64",
                "nginx:bookworm",
            ])
        host = os.getenv("MTV_RAW_ADDR")
        port = os.getenv("MTV_SERVER_PORT")
        uvicorn.run(app, host=host, port=int(port))

    elif args.delete: 
        pid_path = os.getenv("MTV_PID_PATH")
        with open(pid_path, "r") as f:
            pid = f.read()
        if pid:
            subprocess.run(["kill", pid])

        containers = subprocess.run(("docker", "ps", "-aq"))
        for container in containers:
            subprocess.run(("docker", "stop", container))
            subprocess.run(("docker", "rm", container))
        subprocess.run(("sudo", "rm", "-rf", "/usr/share/MTV2"))

if __name__ == "__main__":
    load_dotenv()
    setup()