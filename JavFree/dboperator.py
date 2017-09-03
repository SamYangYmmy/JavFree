 #coding:utf-8
import MySQLdb
from scrapy.utils.project import get_project_settings

class DBOperator():
    # 初始化，得到setting 中的数据库设置：
    def __init__(self):
        self.settings=get_project_settings()
        self.host=self.settings['MYSQL_HOST']
        self.port=self.settings['MYSQL_PORT']
        self.user=self.settings['MYSQL_USER']
        self.passwd=self.settings['MYSQL_PASSWD']
        self.db=self.settings['MYSQL_DBNAME']
        self.createDatabase() #初始化时，如果没有数据库，则创建一个数据库
        self.createTable()    #初始化时，如果没有数据表，则创建一个数据表

        self.conn=self.connectMyDatabase()
        self.cur=self.conn.cursor()

    #链接总库
    def connectDatabase(self):
        conn=MySQLdb.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             passwd=self.passwd,
                             charset='utf8')
        return conn
    #链接指定数据库
    def connectMyDatabase(self):
        conn=MySQLdb.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             passwd=self.passwd,
                             db=self.db,
                             charset='utf8')
        return conn


    def createDatabase(self):
        conn=self.connectDatabase()
        sql="create database if not exists "+self.db
        cur=conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def createTable(self):
        conn = self.connectMyDatabase()
        sql= """create table If Not Exists tbl_movie(
                id char(16) not null,
                movie_name char(128) ,
                view_num int ,
                actress char(32)  ,
                pub_date date ,
                movie_time int,
                tag char(128),
                image_num int);"""
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def insert(self, sql, params):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
        except:
            self.conn.rollback()

    def update(self, sql, *params):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
        except:
            self.conn.rollback()

    def delete(self, sql, *params):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
        except:
            self.conn.rollback()