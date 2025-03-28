#!/usr/bin/env python3
from dotenv import load_dotenv
import mtvmovies
import mtvtvshows
import mtvimages
import mtvtables
import os
import sqlite3
import utils
import yaml

CWD = os.getcwd()

class Main:
    def __init__(self, config):
        load_dotenv()
        self.conn = sqlite3.connect(os.getenv("MTV_DB_PATH"))
        self.cursor = self.conn.cursor()
        self.config = config
        # with open('./config.yaml', 'r') as f:
        #     self.config = yaml.safe_load(f)
        

    def main(self):
    
        try:
            mtvtables.CreateTables(self.config).create_tables()

            movs = utils.mtv_walk_dirs(self.config['Media']["MTV_MOVIES_PATH"])
            mtvmovies.ProcessMovies(movs, self.conn, self.cursor, self.config).process()

            images = utils.img_walk_dirs(self.config['Posters']["MTV_POSTER_PATH"])
            mtvimages.ProcessImages(images, self.conn, self.cursor).process()

            tvshows = utils.mtv_walk_dirs(self.config['Media']["MTV_TV_PATH"])
            mtvtvshows.ProcessTVShows(tvshows, self.conn, self.cursor).process()

            tvimages = utils.tvimg_walk_dirs(self.config['Posters']["MTV_TVPOSTER_PATH"])
            mtvimages.ProcessTVImages(tvimages, self.conn, self.cursor).process()

        except sqlite3.OperationalError as e:
            print(e)
        finally:
            self.conn.close()

if __name__ == "__main__":
    m = Main()
    m.main()
