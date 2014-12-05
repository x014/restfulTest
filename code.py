__author__ = 'Administrator'
# coding: utf-8

import web

render = web.template.render('templates/')
db = web.database(dbn='mysql', user='hano', pw='989802', db='restful')
urls = (
    '/(.*)', 'index'
)

class index:
    def GET(self, name):
        print "it is a get request"
        return render.index(name)
    def POST(self, name):
        print "it is a post request"
        return render.index(name)
    def PUT(self, name):
        print "it is a put request"
        return render.index(name)
    def PATCH(self, name):
        print "it is a patch request"
        return render.index(name)
    def DELETE(self, name):
        print "it is a delete request"
        return render.index(name)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()