#!/usr/bin/env python3

import mtvmovies
import mtvtvshows
import mtvimages
# import mtvtables
import os
import sqlite3
import utils

CWD = os.getcwd()

class UpdateMain:
    def __init__(self, config):
        self.config = config
        self.conn = sqlite3.connect(self.config['DBs']["MTV_DB_PATH"])
        self.cursor = self.conn.cursor()        

    def main(self):
    
        try:
            movlist = utils.mtv_walk_dirs(self.config['Media']["MTV_MOVIES_PATH"])
            dblist = utils.get_mov_paths_from_db(self.config)
            movs = []
            if len(movlist) > len(dblist):
                movs = utils.compare_lists(movlist, dblist)
            if len(movs) > 0:
                print("New files to be added to the database:")
                for file in movs:
                    print(file)
                mtvmovies.ProcessMovies(movs, self.conn, self.cursor, self.config).process()
            else:
                print("No new files to be added to the database.\nNo Movies update needed")

            tvshowslist = utils.mtv_walk_dirs(self.config['Media']["MTV_TV_PATH"])
            tvshowsdblist = utils.get_tv_paths_from_db(self.config)
            tvshows = []
            if len(tvshowslist) > len(tvshowsdblist):
                tvshows = utils.compare_lists(tvshowslist, tvshowsdblist)
            if len(tvshows) > 0:
                print("New files to be added to the database:")
                for file in tvshows:
                    print(file)
                mtvtvshows.ProcessTVShows(tvshows, self.conn, self.cursor).process()
            else:
                print("No new files to be added to the database.\nNo TV Shows update needed")

            images = utils.img_walk_dirs(self.config['Posters']["MTV_POSTER_PATH"])
            imagesdblist = utils.get_mov_paths_from_db(self.config)
            images = []
            if len(images) > len(imagesdblist):
                images = utils.compare_lists(images, imagesdblist)
            if len(images) > 0:
                print("New files to be added to the database:")
                for file in images:
                    print(file)
                mtvimages.ProcessImages(images, self.conn, self.cursor, self.config).process()
            else:
                print("No new files to be added to the database.\nNo Images update needed")


            tvimages = utils.tvimg_walk_dirs(self.config['Posters']["MTV_TVPOSTER_PATH"])
            tvimagesdblist = utils.get_tv_paths_from_db(self.config)
            tvimages = []
            if len(tvimages) > len(tvimagesdblist):
                tvimages = utils.compare_lists(tvimages, tvimagesdblist)
            if len(tvimages) > 0:
                print("New files to be added to the database:")
                for file in tvimages:
                    print(file)
                mtvimages.ProcessTVImages(tvimages, self.conn, self.cursor, self.config).process()
            else:
                print("No new files to be added to the database.\nNo TV Images update needed")

        except sqlite3.OperationalError as e:
            print(e)
        finally:
            self.conn.close()

if __name__ == "__main__":
    m = UpdateMain()
    m.main()
