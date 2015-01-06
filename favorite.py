__author__ = 'Administrator'
# coding: utf-8

import json
import sqlite3
import web


class Books:
    def __init__(self):
        pass

    def GET(self):
        params = web.input(offset=0, limit=10)
        offset = params.offset
        limit = params.limit
        favorites = select_favorite_books(offset, limit)
        print "it is a get request about ", id
        web.header('content-type', 'application/json')
        return json.dumps(favorites)

    def POST(self):
        favorite_info = web.data()
        favorite_info_dict = eval(favorite_info)
        print "it is a post request about ", favorite_info
        rowcount = insert_favorite(favorite_info_dict['book_id'], favorite_info_dict['book_name'])
        print "the result is ", rowcount
        return rowcount


class Book:
    def __init__(self):
        pass

    def GET(self, id):
        favorite = select_favorite_book_by_id(id, 0)
        print "it is a get request about ", id
        web.header('content-type', 'application/json')
        if favorite is None:
            return ""
        else:
            return json.dumps(favorite)

    def DELETE(self, id):
        print "it is a delete request"
        delete_favorite(id, 0)
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


def select_favorite_books(offset, limit):
    sqliteconn = sqlite3.connect("test.db")
    cursor = sqliteconn.cursor()

    sql = "select * from favorite LIMIT ? OFFSET ?"

    cursor.execute(sql, (limit, offset,))
    favorites = cursor.fetchall()
    print "select favorites ", favorites
    favorites_as_dict = []
    for favorite in favorites:
        favorite_as_dict = {
            'book_id': favorite[1],
            'book_name': favorite[2]}
        favorites_as_dict.append(favorite_as_dict)
    sqliteconn.commit()
    cursor.close()
    sqliteconn.close()
    return json.dumps(favorites_as_dict)


def select_favorite_book_by_id(bookid, userid):
    print "bookid = ", bookid
    sqliteconn = sqlite3.connect("test.db")
    cursor = sqliteconn.cursor()
    try:
        sql = "select * from favorite WHERE book_id=? AND user_id = ?"
        cursor.execute(sql, (bookid, userid,))
        favorite = cursor.fetchone()
        if favorite is not None:
            result = {
                'book_id': favorite[1],
                'book_name': favorite[2]}
            return result
    finally:
        sqliteconn.commit()
        cursor.close()
        sqliteconn.close()
    return ""


def delete_favorite(bookid, userid):
    sqliteconn = sqlite3.connect("test.db")
    cursor = sqliteconn.cursor()
    sql_delete = "delete from favorite WHERE book_id=? AND user_id = ?"
    cursor.execute(sql_delete, (bookid, userid))
    sqliteconn.commit()
    cursor.close()
    sqliteconn.close()