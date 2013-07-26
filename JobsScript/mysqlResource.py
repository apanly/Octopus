#coding:utf-8
import MySQLdb
from JobsProject.settings import DATABASES
class mysqlOpe:
    def __init__(self):
        global DATABASES
        host=DATABASES['default']['HOST']
        user=DATABASES['default']['USER']
        passwd=DATABASES['default']['PASSWORD']
        db=DATABASES['default']['NAME']
        port=int(DATABASES['default']['PORT'])
        self.conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,port=port,charset="utf8")

    def select(self,sql):
        cur=self.conn.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute(sql)
        res=cur.fetchall()
        cur.close()
        return res

    def selectone(self,sql):
        cur=self.conn.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute(sql)
        res=cur.fetchone()
        cur.close()
        return res
    def update(self,sql):
        cur=self.conn.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute(sql)
        cur.close()
        self.conn.commit()
    def insert(self,sql):
        cur=self.conn.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute(sql)
        cur.close()
        self.conn.commit()
        return self.conn.insert_id()

    def close(self):
        self.conn.close()
