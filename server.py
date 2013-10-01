#!/usr/bin/env python3
from tornado import websocket, web, ioloop
#import sqlite3 as sql
import configparser as cfgp

cfgarr = None
tasks = []
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
        self.render("templates/index.html", conf=cfgarr, nts=len(tasks))


class AddHandler(web.RequestHandler):
    def get(self):
        self.render("templates/addtask.html", conf=cfgarr, nts=len(tasks))


class TaskHandler(web.RequestHandler):
    def get(self):
        self.render("templates/tasks.html", conf=cfgarr, nts=len(tasks))


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
