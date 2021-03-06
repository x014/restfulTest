__author__ = 'Administrator'
# coding: utf-8

import sqlite3
import json

import web


render = web.template.render('templates/')
urls = (
    '/user/(.*)', 'index',
    '/user_/(.*)', 'index',
    '/cookie', 'cookie',
    '/head', 'head',
    '/auth_head', 'auth_head',
    '/favorite/books/(\d+)', 'favorite.Book',
    '/favorite/books', 'favorite.Books'
    # '/user', 'index2'
)


class index:

    def GET(self, name):
        params = web.input(page=1, size=5)
        page = params.page
        size = params.size
        users = select_user(name, page, size)
        print "it is a get request about ", name
        web.header('content-type', 'application/json')

        return json.dumps(users)

    def POST(self, *name):  # post参数必须跟请求数对应
        user_info = web.data()
        user_info_dict = eval(user_info)
        print "it is a post request about ", user_info
        rowcount = insert_user(user_info_dict['name'], user_info_dict['age'])
        print "the result is ", rowcount
        return rowcount

    def PUT(self, name):
        user_info = web.data()
        user_info_dict = eval(user_info)
        print "it is a put request ", user_info
        insert_user(user_info_dict['name'], user_info_dict['age'])
        return 0

    def PATCH(self, name):
        print "it is a patch request ", name
        user_data = web.data()
        user_info_dict = eval(user_data)
        print user_info_dict
        update_user(user_info_dict['name'], user_info_dict['age'])
        return 0

    def DELETE(self, name):
        print "it is a delete request"
        delete_user(name)
        return 0


class index2:
    def GET(self):
        users = select_user("")
        print "it is a get request about "
        web.header('content-type', 'text/json')
        return json.dumps(users)

    def POST(self):  # post参数必须跟请求数对应
        user_info = web.input(name=None, age=0)
        print "it is a post request about ", user_info
        rowcount = insert_user(user_info.name, user_info.age)
        print "the result is ", rowcount
        return rowcount


class cookie:
    def GET(self):
        cookie = web.cookies()
        result = {'testcookie': cookie.testcookie}
        print 'get cookie test ', cookie
        return json.dumps(result)


class head:
    def GET(self):

        # header = web.ctx.env.get("HTTP_REFERER", "not exist key1")
        header = web.input()
        # result = {'testcookie': header.testcookie}
        print 'get head test ', web.ctx.env
        # return json.dumps(result)

class auth_head:
    def GET(self):
        auth = web.ctx.env.get("HTTP_AUTHORIZATION", "none")
        # header = web.input()
        # result = {'testcookie': header.testcookie}
        print 'get head test ', web.ctx.env
        # return json.dumps(result)
        if auth == 'none':
            raise web.unauthorized()
        else:
            return 1


def init_user():
    sqlite_conn = sqlite3.connect("test.db")
    cursor = sqlite_conn.cursor()
    sql_del = "DROP TABLE IF EXISTS user;"
    cursor.execute(sql_del)
    sql_create_table = "create table user (id varchar(10) primary key,pid varchar(10),name varchar(10) ,age varchar(10))"
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


def select_user(name, page, size):
    sqliteConn = sqlite3.connect("test.db")
    cursor = sqliteConn.cursor()
    sql_insert = "select * from user WHERE name=?"
    sql_insert_all = "select * from user"
    print "test 1 ", name is None
    print "test 2 ", len(name)
    if len(name) == 0:
        cursor.execute(sql_insert_all)
        users = cursor.fetchall()
        user_list = []
        for user in users:
            user_dict = dict()
            user_dict['pid'] = user[0]
            user_dict['name'] = user[1]
            user_dict['age'] = user[2]
            user_list.append(user_dict)
    else:
        cursor.execute(sql_insert, (name,))
        users = cursor.fetchone()
        print "select users ", users
        user_dict = {'name': users[2], 'age': users[3]}
        sqliteConn.commit()
        cursor.close()
        sqliteConn.close()
        return user_dict


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
    insert_user('hano', 13)
    app = web.application(urls, globals())
    app.run()