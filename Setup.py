#!/usr/bin/env python3
import argparse
import main
import os
# import subprocess
from pprint import pprint
# from dotenv import load_dotenv
import utils
import uvicorn
from mtvfastapi import app
import yaml

with open('./config.yaml', 'r') as f:
    config = yaml.safe_load(f)

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

        main.Main(config).main()

        host = config["Server"]["MTV_RAW_ADDR"]
        port = config["Server"]["MTV_SERVER_PORT"]
        uvicorn.run(app, host=host, port=int(port))
        
    elif args.restart:
        pass
        # main.Main().main()
        # host = os.getenv("MTV_RAW_ADDR")
        # port = self.config["Server"]["MTV_SERVER_PORT"]
        # uvicorn.run(app, host=host, port=int(port))

    elif args.update:
        pass
        # host = os.getenv("MTV_RAW_ADDR")
        # port = self.config["Server"]["MTV_SERVER_PORT"]
        # uvicorn.run(app, host=host, port=int(port))

    elif args.delete: 
        pass
        

if __name__ == "__main__":
    setup()