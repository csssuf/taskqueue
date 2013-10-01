#!/usr/bin/env python3
from tornado import websocket, web, ioloop
#import sqlite3 as sql
import configparser as cfgp

cfgarr = None
#sqlconn = sql.connect('db/tasks.db')

def main():
    global cfgarr
    cfgarr = cfgp.ConfigParser()
    cfgarr.read('taskqueue.cfg')
    app = web.Application([
        (r'/', IndexHandler),
        (r'/static/(.*)', web.StaticFileHandler, {'path':
            cfgarr['core']['staticpath']}),
        (r'/addtask', AddHandler),
        (r'/tasks', TaskHandler),
        (r'/ws', WSHandler)
        ])
    app.listen(cfgarr['core']['port'])
    ioloop.IOLoop.instance().start()


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("templates/index.html", conf=cfgarr)


class AddHandler(web.RequestHandler):
    def get(self):
        self.render("templates/addtask.html", conf=cfgarr)


class TaskHandler(web.RequestHandler):
    def get(self):
        self.render("templates/tasks.html", conf=cfgarr)


class WSHandler(websocket.WebSocketHandler):
    lastsent = None
    def open(self):
        print('Websocket opened.')

    def on_message(self, message):
        print('Message received: %s' %(message))

    def on_close(self):
        print('Websocket closed.')

if __name__ == '__main__':
    main()
