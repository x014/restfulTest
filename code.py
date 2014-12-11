__author__ = 'Administrator'
# coding: utf-8

import web
import sqlite3
import json

render = web.template.render('templates/')
urls = (
    '/user/(.*)', 'index',
)


class index:

    def GET(self, name):
        users = select_user(name)
        print "it is a get request about "
        web.header('content-type', 'text/json')
        return json.dumps(users)

    def POST(self, *name):  # post参数必须跟请求数对应
        user_info = web.input(name=None, age=0)
        print "it is a post request about ", user_info
        age = user_info['age']
        rowcount = insert_user(user_info.name, age)
        print "the result is ", rowcount
        return rowcount

    def PUT(self, name):
        user_info = web.input()
        print "it is a put request ", user_info
        insert_user(user_info.name, user_info.age)
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
    cursor.execute(sql_insert, (name, age))
    rowcount = cursor.rowcount
    cursor.close()
    sqliteConn.commit()
    sqliteConn.close()
    return rowcount


def select_user(name):
    sqliteConn = sqlite3.connect("test.db")
    cursor = sqliteConn.cursor()
    sql_insert = "select * from user WHERE name=?"
    cursor.execute(sql_insert, (name,))
    users = cursor.fetchall()
    user_list = []
    for user in users:
        user_dict = dict()
        user_dict['id'] = user[0]
        user_dict['pid'] = user[1]
        user_dict['name'] = user[2]
        user_dict['age'] = user[3]
        user_list.append(user_dict)
    sqliteConn.commit()
    cursor.close()
    sqliteConn.close()
    return user_list


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