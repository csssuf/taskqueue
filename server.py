#!/usr/bin/env python3
from tornado import websocket, web, ioloop
#import sqlite3 as sql
import configparser as cfgp
import utils
import json

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
        ], debug=True)
    app.listen(cfgarr['core']['port'])
    ioloop.IOLoop.instance().start()


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("templates/index.html", conf=cfgarr, nts=len(tasks))


class AddHandler(web.RequestHandler):
    def get(self):
        self.render("templates/addtask.html", conf=cfgarr, nts=len(tasks),
                cf=utils.casefix)


class TaskHandler(web.RequestHandler):
    def get(self):
        self.render("templates/tasks.html", conf=cfgarr, nts=len(tasks),
                tasks=tasks, cf=utils.casefix)


class WSHandler(websocket.WebSocketHandler):
    global tasks
    lastsent = None
    def open(self):
        print('Websocket opened.')
        #self.ping(bytes())

    def on_message(self, message):
        global tasks
        msg = message.split(' ')
        print(msg)
        if msg[0] == 'sudo' and msg[1] == 'delete':
            print('removing' + msg[2])
            toremove = int(msg[2])
            if toremove < len(tasks):
                del(tasks[toremove])
            self.ping(bytes())
        elif msg[0] == 'update':
            self.ping(bytes())
        elif msg[0] == 'addtask':
            print('adding song')
            ratask = ''
            for i in msg[1:]:
                ratask += i + ' '
            ratask = ratask[:len(ratask) - 1]
            ntask = ratask.split('@___@')
            tasks.append(ntask[:len(ntask) - 1])
        #print('Message received: %s' %(message))

    def on_pong(self, data):
        self.write_message(json.dumps(tasks))
        print('pong received')

    def on_close(self):
        print('Websocket closed.')

if __name__ == '__main__':
    main()
