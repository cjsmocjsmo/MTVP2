#!/usr/bin/env python3

import mtvmovies
import mtvtvshows
import mtvimages
import mtvtables
import os
import sqlite3
import utils

CWD = os.getcwd()

class Main:
    def __init__(self, config):
        self.config = config
        self.conn = sqlite3.connect(self.config['DBs']["MTV_DB_PATH"])
        self.cursor = self.conn.cursor()        

    def main(self):
    
        try:
            mtvtables.CreateTables(self.config).create_tables()

            movs = utils.mtv_walk_dirs(self.config['Media']["MTV_MOVIES_PATH"])
            mtvmovies.ProcessMovies(movs, self.conn, self.cursor, self.config).process()

            images = utils.img_walk_dirs(self.config['Posters']["MTV_POSTER_PATH"])
            mtvimages.ProcessImages(images, self.conn, self.cursor, self.config).process()

            tvshows = utils.mtv_walk_dirs(self.config['Media']["MTV_TV_PATH"])
            mtvtvshows.ProcessTVShows(tvshows, self.conn, self.cursor, self.config).process()

            tvimages = utils.tvimg_walk_dirs(self.config['Posters']["MTV_TVPOSTER_PATH"])
            mtvimages.ProcessTVImages(tvimages, self.conn, self.cursor, self.config).process()

        except sqlite3.OperationalError as e:
            print(e)
        finally:
            self.conn.close()

if __name__ == "__main__":
    m = Main()
    m.main()
