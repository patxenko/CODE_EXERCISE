import sqlite3
from sqlite3 import Error
from datetime import datetime
import logging

logger = logging.getLogger('uninvention')


class DB:
    def __init__(self):
        self.dbfile = 'data_cop.db'
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.dbfile)
            cur = self.conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS blocked (group_name TEXT, time TEXT )''')
            self.conn.commit()
        except Error as e:
            logger.error("Error in DB: " + str(e))
            exit()

    def block_group(self, group_name):
        try:
            cur = self.conn.cursor()
            res = cur.execute("SELECT time FROM blocked WHERE group_name =?", (group_name,))
            last_time = res.fetchone()
            if last_time is None:
                # We block it
                sql = ''' INSERT INTO blocked(group_name,time) VALUES(?,?) '''
                cur = self.conn.cursor()
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                cur.execute(sql, (group_name, str(current_time)))
                self.conn.commit()
                return False
            else:
                logger.error("Group {} is blocked, last execution time: {}".format(group_name, last_time))
                exit()
        except Error as e:
            logger.error("Blocking group " + str(e))
            exit()

    def unblock_group(self, group_name):
        try:
            sql = 'DELETE FROM blocked WHERE group_name=?'
            cur = self.conn.cursor()
            cur.execute(sql, (group_name,))
            self.conn.commit()
        except Error as e:
            logger.error("Unblocking group " + str(e))
            exit()
