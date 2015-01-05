__author__ = 'Administrator'
# coding: utf-8

import json
import sqlite3
import web


class Favorite:
    def __init__(self):
        pass

    def GET(self, id):
        params = web.input(page=0, size=10)
        page = params.page
        size = params.size
        favorites = select_favorite(id, page, size)
        print "it is a get request about ", id
        web.header('content-type', 'application/json')
        return json.dumps(favorites)

    def POST(self, *id):  # post参数必须跟请求数对应
        favorite_info = web.data()
        favorite_info_dict = eval(favorite_info)
        print "it is a post request about ", favorite_info
        rowcount = insert_favorite(favorite_info_dict['book_id'], favorite_info_dict['book_name'])
        print "the result is ", rowcount
        return rowcount

    def DELETE(self, id):
        print "it is a delete request"
        delete_favorite(id)
        return 0


def init_favorite():
    sqliteconn = sqlite3.connect("test.db")
    cursor = sqliteconn.cursor()
    sql_del = "DROP TABLE IF EXISTS favorite;"
    cursor.execute(sql_del)
    sql_create_table = "CREATE TABLE [favorite] ([user_id] INT, [book_id] INT, [book_name] CHAR);)"
    cursor.execute(sql_create_table)
    sqliteconn.commit()
    cursor.close()
    sqliteconn.close()


def insert_favorite(book_id, book_name):
    sqliteconn = sqlite3.connect("test.db")
    cursor = sqliteconn.cursor()
    sql_insert = "insert into favorite ('book_id', 'book_name') values (?, ?);"
    cursor.execute(sql_insert, (book_id, book_name.decode('utf-8')))
    rowcount = cursor.rowcount
    cursor.close()
    sqliteconn.commit()
    sqliteconn.close()
    return rowcount


def select_favorite(id, offset, limit):
    sqliteconn = sqlite3.connect("test.db")
    cursor = sqliteconn.cursor()
    # sql = "select * from favorite WHERE name=?"

    sql = "select * from favorite"
    if len(id) >= 1:
        sql += "WHERE name=?"
    sql += " LIMIT ? OFFSET ?"

    print "id is None ? ", id is None
    print "len(id): ", len(id)
    cursor.execute(sql, (id, limit, offset,))
    favorites = cursor.fetchone()
    print "select favorites ", favorites
    favorites_as_dict = []
    for favorite in favorites:
        favorite_as_dict = {
            'book_id': favorite.book_id,
            'book_name': favorite.book_name}
        favorites_as_dict.append(favorite_as_dict)
    sqliteconn.commit()
    cursor.close()
    sqliteconn.close()
    return json.dumps(favorites_as_dict)

def delete_favorite(id):
    sqliteconn = sqlite3.connect("test.db")
    cursor = sqliteconn.cursor()
    sql_delete = "delete from favorite where book_id=?"
    cursor.execute(sql_delete, (id,))
    sqliteconn.commit()
    cursor.close()
    sqliteconn.close()