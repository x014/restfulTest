__author__ = 'Administrator'
# coding: utf-8

import web
import sqlite3

render = web.template.render('templates/')
urls = (
    '/(.*)', 'index'
)


class index:

    def GET(self, name):
        user = select_user("hano")
        print "it is a get request about ", user
        return render.index(name)
    def POST(self, name):
        insert_user(name)
        print "it is a post request about "
        return render.index(name)
    def PUT(self, name):
        insert_user(name)
        print "it is a put request"
        return render.index(name)
    def PATCH(self, name):
        print "it is a patch request"
        return render.index(name)
    def DELETE(self, name):
        print "it is a delete request"
        return render.index(name)


def init_user():
    sqlite_conn = sqlite3.connect("test.db")
    cursor = sqlite_conn.cursor()
    sql_del="DROP TABLE IF EXISTS user;"
    cursor.execute(sql_del)
    sql_create_table = "create table user (id integer primary key,pid integer,name varchar(10) UNIQUE,age integer)"
    cursor.execute(sql_create_table)
    sqlite_conn.commit()
    cursor.close()
    sqlite_conn.close()


def insert_user(name):
    sqliteConn = sqlite3.connect("test.db")
    cursor = sqliteConn.cursor()
    sql_insert = "insert into user (name) values (\'" + name + "\');"
    cursor.execute(sql_insert)
    sqliteConn.commit()
    cursor.close()
    sqliteConn.close()


def select_user(name):
    sqliteConn = sqlite3.connect("test.db")
    cursor = sqliteConn.cursor()
    sql_insert = "select * from user WHERE name=?"
    cursor.execute(sql_insert, (name,))
    users = cursor.fetchall()
    sqliteConn.commit()
    cursor.close()
    sqliteConn.close()
    return users


def update_user(age):
    #"update catalog set name='Boy' where id = 0"



if __name__ == "__main__":
    init_user()
    insert_user("Hano233")
    app = web.application(urls, globals())
    app.run()