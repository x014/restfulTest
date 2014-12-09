__author__ = 'Administrator'
# coding: utf-8

import web
import sqlite3
import json

render = web.template.render('templates/')
urls = (
    '/user', 'index',
    '/user/(.*)', 'index'
)


class index:

    def GET(self, *name):
        user_info = web.input()
        user = select_user(user_info.name)
        print "it is a get request about ", name
        web.header('content-type', 'text/json')
        return json.dumps(user)

    def POST(self, *name):  # post参数必须跟请求数对应
        print "it is a post request about "
        user_info = web.input()
        age = ""
        try:
            age = user_info.age
        except AttributeError, e:
            pass
        rowcount = insert_user(user_info.name, age)
        return rowcount

    def PUT(self):
        user_info = web.input()
        insert_user(user_info.name, user_info.age)
        print "it is a put request"
        return 0

    def PATCH(self):
        print "it is a patch request"
        user_data = web.input()
        print user_data
        update_user(user_data.name, user_data.age)
        return 0

    def DELETE(self):
        print "it is a delete request"
        user_data = web.input()
        delete_user(user_data.name)
        return 0


def init_user():
    sqlite_conn = sqlite3.connect("test.db")
    cursor = sqlite_conn.cursor()
    sql_del="DROP TABLE IF EXISTS user;"
    cursor.execute(sql_del)
    sql_create_table = "create table user (id integer primary key,pid integer,name varchar(10) ,age integer)"
    cursor.execute(sql_create_table)
    sqlite_conn.commit()
    cursor.close()
    sqlite_conn.close()


def insert_user(name, age=0):
    sqliteConn = sqlite3.connect("test.db")
    cursor = sqliteConn.cursor()
    sql_insert = "insert into user (name, age) values (?, ?);"
    rowcount = cursor.execute(sql_insert, (name, age))
    sqliteConn.commit()
    cursor.close()
    sqliteConn.close()
    return rowcount


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


def update_user(name, age):
    sqliteConn = sqlite3.connect("test.db")
    cursor = sqliteConn.cursor()
    update_sql = "update user set age=? where name=?"
    cursor.execute(update_sql, (age, name))
    sqliteConn.commit()
    cursor.close()
    sqliteConn.close()


def delete_user(name):
    sqliteConn = sqlite3.connect("test.db")
    cursor = sqliteConn.cursor()
    sql_delete = "delete from user where name=?"
    cursor.execute(sql_delete, (name,))
    sqliteConn.commit()
    cursor.close()
    sqliteConn.close()


if __name__ == "__main__":
    init_user()
    app = web.application(urls, globals())
    app.run()